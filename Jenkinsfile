pipeline {
    agent any

    environment {
        PYTHON = "C:\\Users\\reshma.b\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
    }

    stages {

        stage('Checkout') {
            steps {
                cleanWs()
                git branch: 'main', url: 'https://github.com/reshmababu627/Automation-Playwright.git'
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

        stage('Run Tests in Parallel') {
            parallel {

                stage('Login Test') {
                    steps {
                        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                            bat "%PYTHON% -m pytest tests/test_login.py --reruns 2 --reruns-delay 2 --alluredir=allure-results"
                        }
                    }
                }

                stage('Employment Test') {
                    steps {
                        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                            bat "%PYTHON% -m pytest tests/test_employment_status.py --reruns 2 --reruns-delay 2 --alluredir=allure-results"
                        }
                    }
                }

                stage('General Info') {
                    steps {
                        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                            bat "%PYTHON% -m pytest tests/test_general_info.py --reruns 2 --reruns-delay 2 --alluredir=allure-results"
                        }
                    }
                }

                stage('Job Actions') {
                    steps {
                        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                            bat "%PYTHON% -m pytest tests/test_job_actions.py --reruns 2 --reruns-delay 2 --alluredir=allure-results"
                        }
                    }
                }

                stage('Job Categories') {
                    steps {
                        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                            bat "%PYTHON% -m pytest tests/test_job_categories.py --reruns 2 --reruns-delay 2 --alluredir=allure-results"
                        }
                    }
                }

                stage('Locations') {
                    steps {
                        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                            bat "%PYTHON% -m pytest tests/test_locations.py --reruns 2 --reruns-delay 2 --alluredir=allure-results"
                        }
                    }
                }

                stage('User Management') {
                    steps {
                        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                            bat "%PYTHON% -m pytest tests/test_user_management.py --reruns 2 --reruns-delay 2 --alluredir=allure-results"
                        }
                    }
                }

                stage('Workshift') {
                    steps {
                        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                            bat "%PYTHON% -m pytest tests/test_work_shifts.py --reruns 2 --reruns-delay 2 --alluredir=allure-results"
                        }
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
        always {
            archiveArtifacts artifacts: 'allure-results/**', fingerprint: true
        }
        failure {
            emailext to: 'reshmababu162@gmail.com',
                     subject: "Jenkins Build Failed",
                     body: "Build failed. Please check the Jenkins console and Allure report."
        }
    }
}