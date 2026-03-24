pipeline {
    agent any

    tools {
        allure 'allure'
    }

    environment {
        PYTHON = "C:\\Users\\reshma.b\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
    }

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/reshmababu627/Automation-Playwright.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat "\"%PYTHON%\" -m pip install -r requirements.txt"
                bat "\"%PYTHON%\" -m playwright install"
                bat "\"%PYTHON%\" -m pip install pytest-rerunfailures"
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
                        bat "\"%PYTHON%\" -m pytest tests/test_login.py --reruns 2 --reruns-delay 2 --alluredir=allure-results/login"
                    }
                }

                stage('Employment Test') {
                    steps {
                        bat "\"%PYTHON%\" -m pytest tests/test_employment_status.py --reruns 2 --reruns-delay 2 --alluredir=allure-results/employment"
                    }
                }

                stage('General Info') {
                    steps {
                        bat "\"%PYTHON%\" -m pytest tests/test_general_info.py --reruns 2 --reruns-delay 2 --alluredir=allure-results/general"
                    }
                }

                stage('Job Actions') {
                    steps {
                        bat "\"%PYTHON%\" -m pytest tests/test_job_actions.py --reruns 2 --reruns-delay 2 --alluredir=allure-results/job"
                    }
                }

                stage('Job Categories') {
                    steps {
                        bat "\"%PYTHON%\" -m pytest tests/test_job_categories.py --reruns 2 --reruns-delay 2 --alluredir=allure-results/jobcat"
                    }
                }

                stage('Locations') {
                    steps {
                        bat "\"%PYTHON%\" -m pytest tests/test_locations.py --reruns 2 --reruns-delay 2 --alluredir=allure-results/location"
                    }
                }

                stage('User Management') {
                    steps {
                        bat "\"%PYTHON%\" -m pytest tests/test_user_management.py --reruns 2 --reruns-delay 2 --alluredir=allure-results/user"
                    }
                }

                stage('Workshift') {
                    steps {
                        bat "\"%PYTHON%\" -m pytest tests/test_work_shifts.py --reruns 2 --reruns-delay 2 --alluredir=allure-results/workshift"
                    }
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }

    post {
        always {
            emailext (
                subject: "Build: ${env.JOB_NAME} - #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
                body: """
                Build Status: ${currentBuild.currentResult}
                
                Job Name: ${env.JOB_NAME}
                Build Number: ${env.BUILD_NUMBER}
                
                Check Report: ${env.BUILD_URL}
                """,
                to: "reshmababu162@gmail.com"
            )
        }
    }
}