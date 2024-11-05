pipeline {
    agent any
    environment {
        CODECOV_TOKEN = credentials('codecov-token') 
    }
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/schnitz-air/Prisma_API_scripts', branch: 'main'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'npm install' // Adjust according to your package manager
            }
        }
        stage('Run Tests') {
            steps {
                sh 'npm test' // Run tests and generate coverage report
            }
        }
        stage('Upload Coverage to Codecov') {
            steps {
                sh 'bash <(curl -s https://codecov.io/bash)' 
            }
        }
    }
    post {
        always {
            cleanWs() // Clean the workspace after build
        }
    }
}
