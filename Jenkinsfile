
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'username/simple-node-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_CREDENTIALS = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                // Pobranie kodu z repozytorium
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // Instalacja zależności Node.js
                sh 'npm install'
            }
        }

        stage('Run Tests') {
            steps {
                // Uruchomienie testów
                sh 'npm test'
            }
        }

        stage('Build Application') {
            steps {
                // Budowanie aplikacji
                sh 'npm run build'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Budowanie obrazu Docker
                sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
            }
        }

        stage('Push Docker Image') {
            steps {
                // Logowanie i publikowanie obrazu do Docker Hub
                withCredentials([
                    usernamePassword(
                        credentialsId: "${DOCKER_CREDENTIALS}",
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                            -u "$DOCKER_USER" --password-stdin

                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}

                        docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline zakończony pomyślnie!'
        }

        failure {
            echo 'Pipeline zakończony błędem!'
        }

        always {
            echo 'Zakończono wykonywanie pipeline.'
        }
    }
}
