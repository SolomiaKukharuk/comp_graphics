#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>

<<<<<<< Updated upstream
int main(void)
=======
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

GLuint createProgram(const char* vertexShaderSource, const char* fragmentShaderSource)
{
    GLint success;
    char infoLog[512];

    GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
    glCompileShader(vertexShader);

    glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
    if (!success)
        glGetShaderInfoLog(vertexShader, 512, NULL, infoLog);

    GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
    glCompileShader(fragmentShader);

    glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &success);
    if (!success)
        glGetShaderInfoLog(fragmentShader, 512, NULL, infoLog);

    GLuint shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);

    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);

    return shaderProgram;
}

GLuint loadTexture(const char* path)
{
    GLuint texture;
    glGenTextures(1, &texture);
    glBindTexture(GL_TEXTURE_2D, texture);

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
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

int main()
>>>>>>> Stashed changes
{
    GLFWwindow* window;

    if (!glfwInit())
        return -1;

    int windowWidth = 800;
    int windowHeight = 600;

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

<<<<<<< Updated upstream
    window = glfwCreateWindow(640, 480, "Hello World", NULL, NULL);
=======
    window = glfwCreateWindow(windowWidth, windowHeight, "Keyboard and Mouse Rectangle", NULL, NULL);

>>>>>>> Stashed changes
    if (!window)
    {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window);
    if (!gladLoadGLLoader((GLADloadproc) glfwGetProcAddress)) {
        std::cout << "Failed to initialize GLAD" << std::endl;
        return -1;
    }

    glClearColor(1.0, 0.0, 0.0, 1.0);

<<<<<<< Updated upstream
    while (!glfwWindowShouldClose(window) && !glfwGetKey(window, GLFW_KEY_ESCAPE))
    {
        glClear(GL_COLOR_BUFFER_BIT);
=======
    auto vertexShaderName = R"(
        #version 330 core

        in vec2 aPos;
        in vec2 aTexCoord;

        out vec2 TexCoord;

        uniform vec2 uShift;
        uniform float uAngle;

        void main()
        {
            float c = cos(uAngle);
            float s = sin(uAngle);

            vec2 rotated;
            rotated.x = aPos.x * c - aPos.y * s;
            rotated.y = aPos.x * s + aPos.y * c;

            gl_Position = vec4(rotated + uShift, 0.0, 1.0);
            TexCoord = aTexCoord;
        }
    )";

    auto fragmentShaderName = R"(
        #version 330 core

        in vec2 TexCoord;
        out vec4 FragColor;

        uniform sampler2D texture1;

        void main()
        {
            FragColor = texture(texture1, TexCoord);
        }
    )";

    GLuint shaderProgram = createProgram(vertexShaderName, fragmentShaderName);

    float halfWidth = 0.3f;
    float halfHeight = 0.2f;

    float vertices[] = {
        -halfWidth,  halfHeight,  0.0f, 1.0f,
         halfWidth,  halfHeight,  1.0f, 1.0f,
         halfWidth, -halfHeight,  1.0f, 0.0f,
        -halfWidth, -halfHeight,  0.0f, 0.0f
    };

    unsigned int indices[] = {
        0, 1, 2,
        0, 2, 3
    };

    GLuint VAO, VBO, EBO;

    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glGenBuffers(1, &EBO);

    glBindVertexArray(VAO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

    GLuint posLocation = glGetAttribLocation(shaderProgram, "aPos");
    glVertexAttribPointer(posLocation, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(posLocation);

    GLuint texLocation = glGetAttribLocation(shaderProgram, "aTexCoord");
    glVertexAttribPointer(texLocation, 2, GL_FLOAT, GL_FALSE, 4 * sizeof(float), (void*)(2 * sizeof(float)));
    glEnableVertexAttribArray(texLocation);

    glBindVertexArray(0);

    GLuint texture1 = loadTexture("textures/texture2.jpg");

    glUseProgram(shaderProgram);
    glUniform1i(glGetUniformLocation(shaderProgram, "texture1"), 0);

    GLint shiftUniformPos = glGetUniformLocation(shaderProgram, "uShift");
    GLint angleUniformPos = glGetUniformLocation(shaderProgram, "uAngle");

    float shiftX = 0.0f;
    float shiftY = 0.0f;
    float angle = 0.0f;

    const float moveSpeed = 1.0f;
    const float rotationSpeed = 3.0f;

    double lastTime = glfwGetTime();
    const double frameTime = 1.0 / 60.0;

    while (!glfwWindowShouldClose(window) && glfwGetKey(window, GLFW_KEY_ESCAPE) != GLFW_PRESS)
    {
        double frameStart = glfwGetTime();

        double currentTime = glfwGetTime();
        float deltaTime = static_cast<float>(currentTime - lastTime);
        lastTime = currentTime;

        if (glfwGetKey(window, GLFW_KEY_LEFT) == GLFW_PRESS)
            shiftX -= moveSpeed * deltaTime;

        if (glfwGetKey(window, GLFW_KEY_RIGHT) == GLFW_PRESS)
            shiftX += moveSpeed * deltaTime;

        if (glfwGetKey(window, GLFW_KEY_UP) == GLFW_PRESS)
            shiftY += moveSpeed * deltaTime;

        if (glfwGetKey(window, GLFW_KEY_DOWN) == GLFW_PRESS)
            shiftY -= moveSpeed * deltaTime;

        double mouseX, mouseY;
        glfwGetCursorPos(window, &mouseX, &mouseY);

        float normalizedMouseX = static_cast<float>(mouseX / windowWidth * 2.0 - 1.0);
        float normalizedMouseY = static_cast<float>(1.0 - mouseY / windowHeight * 2.0);

        bool mouseOnRectangle =
            normalizedMouseX >= shiftX - halfWidth &&
            normalizedMouseX <= shiftX + halfWidth &&
            normalizedMouseY >= shiftY - halfHeight &&
            normalizedMouseY <= shiftY + halfHeight;

        if (mouseOnRectangle)
            angle += rotationSpeed * deltaTime;

        glClear(GL_COLOR_BUFFER_BIT);

        glUseProgram(shaderProgram);
        glUniform2f(shiftUniformPos, shiftX, shiftY);
        glUniform1f(angleUniformPos, angle);

        glActiveTexture(GL_TEXTURE0);
        glBindTexture(GL_TEXTURE_2D, texture1);

        glBindVertexArray(VAO);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);

>>>>>>> Stashed changes
        glfwSwapBuffers(window);

        glfwPollEvents();
    }

    glfwTerminate();
    return 0;
}