
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
                branch 'main'
            }

            steps {
                sh 'docker compose -p expense-manager-devops up -d --no-build --force-recreate web'
            }
        }
    }
}
