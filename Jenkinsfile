pipeline {

    agent any

    stages {
        stage('Test Django'){
            steps{
                sh "invoke prod.testDjango --echo"
            }
        }
    }

}
