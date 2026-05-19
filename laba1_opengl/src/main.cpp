#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <vector>
#include <cmath>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

const int WIDTH = 900;
const int HEIGHT = 700;

glm::vec3 cameraPos(0.0f, 0.0f, 7.0f);
glm::vec3 cameraFront(0.0f, 0.0f, -1.0f);
glm::vec3 cameraUp(0.0f, 1.0f, 0.0f);

float yaw = -90.0f;
float pitch = 0.0f;
float lastX = WIDTH / 2.0f;
float lastY = HEIGHT / 2.0f;
bool firstMouse = true;

int activeCube = 0;

struct Cube
{
    glm::vec3 position;
    glm::vec3 scale;
    GLuint texture;
};

GLuint createProgram(const char* vertexSource, const char* fragmentSource)
{
    GLint success;
    char infoLog[512];

    GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader, 1, &vertexSource, NULL);
    glCompileShader(vertexShader);

    glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
    if (!success)
    {
        glGetShaderInfoLog(vertexShader, 512, NULL, infoLog);
        std::cout << "Vertex shader error:\n" << infoLog << std::endl;
    }

    GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragmentShader, 1, &fragmentSource, NULL);
    glCompileShader(fragmentShader);

    glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &success);
    if (!success)
    {
        glGetShaderInfoLog(fragmentShader, 512, NULL, infoLog);
        std::cout << "Fragment shader error:\n" << infoLog << std::endl;
    }

    GLuint program = glCreateProgram();
    glAttachShader(program, vertexShader);
    glAttachShader(program, fragmentShader);
    glLinkProgram(program);

    glGetProgramiv(program, GL_LINK_STATUS, &success);
    if (!success)
    {
        glGetProgramInfoLog(program, 512, NULL, infoLog);
        std::cout << "Program link error:\n" << infoLog << std::endl;
    }

    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);

    return program;
}

GLuint loadTexture(const char* path)
{
    GLuint texture;
    glGenTextures(1, &texture);
    glBindTexture(GL_TEXTURE_2D, texture);

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

    int width, height, channels;
    stbi_set_flip_vertically_on_load(true);

    unsigned char* data = stbi_load(path, &width, &height, &channels, 0);

    if (data)
    {
        GLenum format = GL_RGB;

        if (channels == 1)
            format = GL_RED;
        else if (channels == 3)
            format = GL_RGB;
        else if (channels == 4)
            format = GL_RGBA;

        glTexImage2D(GL_TEXTURE_2D, 0, format, width, height, 0, format, GL_UNSIGNED_BYTE, data);
        glGenerateMipmap(GL_TEXTURE_2D);
    }
    else
    {
        std::cout << "Failed to load texture: " << path << std::endl;
    }

    stbi_image_free(data);
    return texture;
}

void mouse_callback(GLFWwindow* window, double xpos, double ypos)
{
    if (glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_RIGHT) != GLFW_PRESS)
        return;

    if (firstMouse)
    {
        lastX = xpos;
        lastY = ypos;
        firstMouse = false;
    }

    float xoffset = xpos - lastX;
    float yoffset = lastY - ypos;

    lastX = xpos;
    lastY = ypos;

    float sensitivity = 0.1f;
    xoffset *= sensitivity;
    yoffset *= sensitivity;

    yaw += xoffset;
    pitch += yoffset;

    if (pitch > 89.0f)
        pitch = 89.0f;

    if (pitch < -89.0f)
        pitch = -89.0f;

    glm::vec3 direction;
    direction.x = cos(glm::radians(yaw)) * cos(glm::radians(pitch));
    direction.y = sin(glm::radians(pitch));
    direction.z = sin(glm::radians(yaw)) * cos(glm::radians(pitch));

    cameraFront = glm::normalize(direction);
}

void processInput(GLFWwindow* window, float deltaTime)
{
    float speed = 4.0f * deltaTime;
    glm::vec3 right = glm::normalize(glm::cross(cameraFront, cameraUp));

    if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)
        cameraPos += speed * cameraFront;

    if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS)
        cameraPos -= speed * cameraFront;

    if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS)
        cameraPos -= right * speed;

    if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS)
        cameraPos += right * speed;

    if (glfwGetKey(window, GLFW_KEY_Q) == GLFW_PRESS)
        cameraPos -= cameraUp * speed;

    if (glfwGetKey(window, GLFW_KEY_E) == GLFW_PRESS)
        cameraPos += cameraUp * speed;

    if (glfwGetKey(window, GLFW_KEY_1) == GLFW_PRESS)
        activeCube = 0;

    if (glfwGetKey(window, GLFW_KEY_2) == GLFW_PRESS)
        activeCube = 1;

    if (glfwGetKey(window, GLFW_KEY_3) == GLFW_PRESS)
        activeCube = 2;
}

int main()
{
    if (!glfwInit())
        return -1;

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    glfwWindowHint(GLFW_STENCIL_BITS, 8);

    GLFWwindow* window = glfwCreateWindow(WIDTH, HEIGHT, "Textured Cubes With Outline", NULL, NULL);

    if (!window)
    {
        std::cout << "Failed to create window" << std::endl;
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window);
    glfwSetCursorPosCallback(window, mouse_callback);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
    {
        std::cout << "Failed to initialize GLAD" << std::endl;
        return -1;
    }

    glViewport(0, 0, WIDTH, HEIGHT);

    glEnable(GL_DEPTH_TEST);
    glEnable(GL_STENCIL_TEST);

    const char* cubeVertexShader = R"(
        #version 330 core

        in vec3 aPos;
        in vec2 aTexCoord;

        out vec2 TexCoord;

        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;

        void main()
        {
            gl_Position = projection * view * model * vec4(aPos, 1.0);
            TexCoord = aTexCoord;
        }
    )";

    const char* cubeFragmentShader = R"(
        #version 330 core

        in vec2 TexCoord;
        out vec4 FragColor;

        uniform sampler2D texture1;

        void main()
        {
            FragColor = texture(texture1, TexCoord);
        }
    )";

    const char* lineVertexShader = R"(
        #version 330 core

        in vec3 aPos;

        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;

        void main()
        {
            gl_Position = projection * view * model * vec4(aPos, 1.0);
        }
    )";

    const char* lineFragmentShader = R"(
        #version 330 core

        out vec4 FragColor;

        void main()
        {
            FragColor = vec4(1.0, 0.18, 0.0, 1.0);
        }
    )";

    GLuint cubeProgram = createProgram(cubeVertexShader, cubeFragmentShader);
    GLuint lineProgram = createProgram(lineVertexShader, lineFragmentShader);

    float cubeVertices[] = {
        -0.5f,-0.5f,-0.5f, 0.0f,0.0f,
         0.5f,-0.5f,-0.5f, 1.0f,0.0f,
         0.5f, 0.5f,-0.5f, 1.0f,1.0f,
         0.5f, 0.5f,-0.5f, 1.0f,1.0f,
        -0.5f, 0.5f,-0.5f, 0.0f,1.0f,
        -0.5f,-0.5f,-0.5f, 0.0f,0.0f,

        -0.5f,-0.5f, 0.5f, 0.0f,0.0f,
         0.5f,-0.5f, 0.5f, 1.0f,0.0f,
         0.5f, 0.5f, 0.5f, 1.0f,1.0f,
         0.5f, 0.5f, 0.5f, 1.0f,1.0f,
        -0.5f, 0.5f, 0.5f, 0.0f,1.0f,
        -0.5f,-0.5f, 0.5f, 0.0f,0.0f,

        -0.5f, 0.5f, 0.5f, 1.0f,0.0f,
        -0.5f, 0.5f,-0.5f, 1.0f,1.0f,
        -0.5f,-0.5f,-0.5f, 0.0f,1.0f,
        -0.5f,-0.5f,-0.5f, 0.0f,1.0f,
        -0.5f,-0.5f, 0.5f, 0.0f,0.0f,
        -0.5f, 0.5f, 0.5f, 1.0f,0.0f,

         0.5f, 0.5f, 0.5f, 1.0f,0.0f,
         0.5f, 0.5f,-0.5f, 1.0f,1.0f,
         0.5f,-0.5f,-0.5f, 0.0f,1.0f,
         0.5f,-0.5f,-0.5f, 0.0f,1.0f,
         0.5f,-0.5f, 0.5f, 0.0f,0.0f,
         0.5f, 0.5f, 0.5f, 1.0f,0.0f,

        -0.5f,-0.5f,-0.5f, 0.0f,1.0f,
         0.5f,-0.5f,-0.5f, 1.0f,1.0f,
         0.5f,-0.5f, 0.5f, 1.0f,0.0f,
         0.5f,-0.5f, 0.5f, 1.0f,0.0f,
        -0.5f,-0.5f, 0.5f, 0.0f,0.0f,
        -0.5f,-0.5f,-0.5f, 0.0f,1.0f,

        -0.5f, 0.5f,-0.5f, 0.0f,1.0f,
         0.5f, 0.5f,-0.5f, 1.0f,1.0f,
         0.5f, 0.5f, 0.5f, 1.0f,0.0f,
         0.5f, 0.5f, 0.5f, 1.0f,0.0f,
        -0.5f, 0.5f, 0.5f, 0.0f,0.0f,
        -0.5f, 0.5f,-0.5f, 0.0f,1.0f
    };

    float outlineVertices[] = {
        -0.5f, -0.5f, -0.5f,
         0.5f, -0.5f, -0.5f,
         0.5f,  0.5f, -0.5f,
        -0.5f,  0.5f, -0.5f,

        -0.5f, -0.5f,  0.5f,
         0.5f, -0.5f,  0.5f,
         0.5f,  0.5f,  0.5f,
        -0.5f,  0.5f,  0.5f
    };

    unsigned int outlineIndices[] = {
        0, 1,  1, 2,  2, 3,  3, 0,
        4, 5,  5, 6,  6, 7,  7, 4,
        0, 4,  1, 5,  2, 6,  3, 7
    };

    GLuint cubeVAO, cubeVBO;
    glGenVertexArrays(1, &cubeVAO);
    glGenBuffers(1, &cubeVBO);

    glBindVertexArray(cubeVAO);
    glBindBuffer(GL_ARRAY_BUFFER, cubeVBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(cubeVertices), cubeVertices, GL_STATIC_DRAW);

    GLuint posLoc = glGetAttribLocation(cubeProgram, "aPos");
    glVertexAttribPointer(posLoc, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(posLoc);

    GLuint texLoc = glGetAttribLocation(cubeProgram, "aTexCoord");
    glVertexAttribPointer(texLoc, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(texLoc);

    GLuint outlineVAO, outlineVBO, outlineEBO;
    glGenVertexArrays(1, &outlineVAO);
    glGenBuffers(1, &outlineVBO);
    glGenBuffers(1, &outlineEBO);

    glBindVertexArray(outlineVAO);

    glBindBuffer(GL_ARRAY_BUFFER, outlineVBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(outlineVertices), outlineVertices, GL_STATIC_DRAW);

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, outlineEBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(outlineIndices), outlineIndices, GL_STATIC_DRAW);

    GLuint linePosLoc = glGetAttribLocation(lineProgram, "aPos");
    glVertexAttribPointer(linePosLoc, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(linePosLoc);

    glBindVertexArray(0);

    GLuint tex1 = loadTexture("textures/texture1.jpg");
    GLuint tex2 = loadTexture("textures/texture2.jpg");
    GLuint tex3 = loadTexture("textures/texture3.jpg");

    std::vector<Cube> cubes = {
        { glm::vec3(-2.0f, 0.0f, 0.0f), glm::vec3(1.0f, 1.0f, 1.0f), tex1 },
        { glm::vec3( 0.2f, 0.4f,-1.5f), glm::vec3(0.9f, 1.2f, 0.9f), tex2 },
        { glm::vec3( 2.2f,-0.3f, 0.4f), glm::vec3(1.1f, 0.8f, 1.1f), tex3 }
    };

    float lastTime = glfwGetTime();

    while (!glfwWindowShouldClose(window))
    {
        float currentTime = glfwGetTime();
        float deltaTime = currentTime - lastTime;
        lastTime = currentTime;

        if (glfwGetMouseButton(window, GLFW_MOUSE_BUTTON_RIGHT) == GLFW_RELEASE)
            firstMouse = true;

        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
            glfwSetWindowShouldClose(window, true);

        processInput(window, deltaTime);

        glm::mat4 view = glm::lookAt(cameraPos, cameraPos + cameraFront, cameraUp);
        glm::mat4 projection = glm::perspective(glm::radians(60.0f), (float)WIDTH / HEIGHT, 0.1f, 100.0f);

        glClearColor(0.1f, 0.12f, 0.16f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);

        glUseProgram(cubeProgram);
        glUniformMatrix4fv(glGetUniformLocation(cubeProgram, "view"), 1, GL_FALSE, glm::value_ptr(view));
        glUniformMatrix4fv(glGetUniformLocation(cubeProgram, "projection"), 1, GL_FALSE, glm::value_ptr(projection));
        glUniform1i(glGetUniformLocation(cubeProgram, "texture1"), 0);

        glBindVertexArray(cubeVAO);

        for (int i = 0; i < cubes.size(); i++)
        {
            glm::mat4 model(1.0f);
            model = glm::translate(model, cubes[i].position);

            if (i == activeCube)
                model = glm::rotate(model, currentTime, glm::vec3(0.2f, 1.0f, 0.3f));

            model = glm::scale(model, cubes[i].scale);

            glUniformMatrix4fv(glGetUniformLocation(cubeProgram, "model"), 1, GL_FALSE, glm::value_ptr(model));

            glActiveTexture(GL_TEXTURE0);
            glBindTexture(GL_TEXTURE_2D, cubes[i].texture);

            glDrawArrays(GL_TRIANGLES, 0, 36);
        }

        glUseProgram(lineProgram);
        glUniformMatrix4fv(glGetUniformLocation(lineProgram, "view"), 1, GL_FALSE, glm::value_ptr(view));
        glUniformMatrix4fv(glGetUniformLocation(lineProgram, "projection"), 1, GL_FALSE, glm::value_ptr(projection));

        glm::mat4 outlineModel(1.0f);
        outlineModel = glm::translate(outlineModel, cubes[activeCube].position);
        outlineModel = glm::rotate(outlineModel, currentTime, glm::vec3(0.2f, 1.0f, 0.3f));
        outlineModel = glm::scale(outlineModel, cubes[activeCube].scale * 1.01f);

        glUniformMatrix4fv(glGetUniformLocation(lineProgram, "model"), 1, GL_FALSE, glm::value_ptr(outlineModel));

        glBindVertexArray(outlineVAO);
        glLineWidth(4.0f);
        glDrawElements(GL_LINES, 24, GL_UNSIGNED_INT, 0);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteVertexArrays(1, &cubeVAO);
    glDeleteBuffers(1, &cubeVBO);

    glDeleteVertexArrays(1, &outlineVAO);
    glDeleteBuffers(1, &outlineVBO);
    glDeleteBuffers(1, &outlineEBO);

    glDeleteTextures(1, &tex1);
    glDeleteTextures(1, &tex2);
    glDeleteTextures(1, &tex3);

    glDeleteProgram(cubeProgram);
    glDeleteProgram(lineProgram);

    glfwTerminate();
    return 0;
}