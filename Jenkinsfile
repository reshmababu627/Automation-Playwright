pipeline {
    agent any

    environment {
        // Define the absolute path to Python on the build agent to avoid PATH issues
        PYTHON = 'C:\\Users\\reshma.b\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {
        stage('Checkout & Clean') {
            steps {
                checkout scm
                // Clear old allure-results to avoid stale reporting
                bat '''
                if exist allure-results rmdir /s /q allure-results
                mkdir allure-results
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                // Use the absolute path to Python to invoke pip
                bat '"%PYTHON%" -m pip install -r requirements.txt'
                bat '"%PYTHON%" -m playwright install chromium'
            }
        }

        stage('Run Tests (Parallel)') {
            steps {
                script {
                    // Use catchError to ensure the pipeline continues even if tests fail
                    catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                        // -n 4 runs tests in parallel using 4 workers for stability on the demo server
                        bat '"%PYTHON%" -m pytest -n auto tests/ --alluredir=allure-results'
                    }
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                // Generates the Allure HTML report from the results
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            // Archive results for manual inspection if needed
            archiveArtifacts artifacts: 'allure-results/*', followSymlinks: false
            cleanWs()
        }
    }
}


