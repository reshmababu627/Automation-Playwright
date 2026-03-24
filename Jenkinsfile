pipeline {
    agent any

    environment {
        PYTHON = "C:\\Users\\reshma.b\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
    }

    stages {

        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat """
                %PYTHON% -m pip install -r requirements.txt
                %PYTHON% -m pip install pytest-rerunfailures
                %PYTHON% -m playwright install
                """
            }
        }

        stage('Clean Results') {
            steps {
                bat '''
                if exist allure-results rmdir /s /q allure-results
                mkdir allure-results
                '''
            }
        }

        stage('Run Tests') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    bat "%PYTHON% -m pytest tests/ -n auto --dist loadfile --reruns 2 --reruns-delay 2 --alluredir=allure-results"
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'allure-results/**', fingerprint: true
        }
    }
}