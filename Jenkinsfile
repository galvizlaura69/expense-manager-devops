
pipeline {

    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    options {
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker compose -p expense-manager-devops build web'
            }
        }

        stage('Django Check') {
            steps {
                sh 'docker compose -p expense-manager-devops run --rm web python manage.py check'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker compose -p expense-manager-devops run --rm web python manage.py test'
            }
        }

        stage('Deploy') {
            when {
                expression {
                    env.BRANCH_NAME == 'main' ||
                    env.GIT_BRANCH == 'origin/main' ||
                    env.GIT_BRANCH == 'main'
                }
            }

            steps {
                echo 'Desplegando versión de producción desde main...'

                sh 'docker compose -p expense-manager-devops up -d --no-build web'

                echo 'Despliegue finalizado.'
            }
        }
    }
}
