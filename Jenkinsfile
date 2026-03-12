pipeline {
    agent any

    environment {
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
                bat 'playwright install chromium'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'pytest tests/test_pay_grades.py --alluredir=allure-results'
            }
            post {
                always {
                    script {
                        // Optional: Publish Allure Report if plugin is installed
                        // allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
                    }
                }
            }
        }

        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'allure-results/*', followSymlinks: false
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
