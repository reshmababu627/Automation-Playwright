pipeline {
    agent any

    tools {
        allure 'allure'
    }

    environment {
        EMAIL_RECIPIENT = 'reshmababu162@gmail.com'
        PYTHON = "C:\\Users\\reshma.b\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/reshmababu627/Automation-Playwright.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat "\"${PYTHON}\" -m pip install -r requirements.txt"
            }
        }

        stage('Clean Results') {
            steps {
                bat 'if exist allure-results rmdir /s /q allure-results'
                bat 'mkdir allure-results'
            }
        }

        stage('Run Tests in Parallel') {
            parallel {

                stage('Login Test') {
                    steps {
                        bat "\"${PYTHON}\" -m pytest tests/test_login.py --alluredir=allure-results"
                    }
                }

                stage('Employment Test') {
                    steps {
                        bat "\"${PYTHON}\" -m pytest tests/test_employment_status.py --alluredir=allure-results"
                    }
                }

                stage('General Info') {
                    steps {
                        bat "\"${PYTHON}\" -m pytest tests/test_general_info.py --alluredir=allure-results"
                    }
                }

                stage('Job Actions') {
                    steps {
                        bat "\"${PYTHON}\" -m pytest tests/test_job_actions.py --alluredir=allure-results"
                    }
                }

                stage('Job Categories') {
                    steps {
                        bat "\"${PYTHON}\" -m pytest tests/test_job_categories.py --alluredir=allure-results"
                    }
                }

                stage('Locations') {
                    steps {
                        bat "\"${PYTHON}\" -m pytest tests/test_locations.py --alluredir=allure-results"
                    }
                }

                stage('User Management') {
                    steps {
                        bat "\"${PYTHON}\" -m pytest tests/test_user_management.py --alluredir=allure-results"
                    }
                }

                stage('Workshift') {
                    steps {
                        bat "\"${PYTHON}\" -m pytest tests/test_work_shifts.py --alluredir=allure-results"
                    }
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

        success {
            emailext (
                subject: "SUCCESS: Build #${BUILD_NUMBER}",
                body: "Build Passed. Check Allure Report in Jenkins.",
                to: "${EMAIL_RECIPIENT}"
            )
        }

        failure {
            emailext (
                subject: "FAILURE: Build #${BUILD_NUMBER}",
                body: "Build Failed. Check console logs.",
                to: "${EMAIL_RECIPIENT}"
            )
        }
    }
}