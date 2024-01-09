pipeline {
    agent any
    // environment{
    //     STRIPE_LIVE_SECRET_KEY= credntials('71fd6a80-3881-44c8-8f95-c841101560a7')
    // }
    
    stages {

            stage('build') {
                options {
                    timeout(time: 60, unit: 'SECONDS') 
                            }
                steps {
                    withCredentials([usernamePassword(credentials: 'STRIPE_TEST_SECRET_KEY', usernameVariable: User, passwordVariable:PWD)]){
                        echo " username is ${User} and password${PWD}"
                    }
                    echo "clone successfull"
                    sh " docker compose up --build" 
                    
                }
            }
            
        }

    post {
            always {
                echo "running build"
            }
            success{
                echo "finish building"
            }
            failure {
                    echo "failed"
                }
        }
}
