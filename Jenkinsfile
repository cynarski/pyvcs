pipeline {
    agent { label 'linux-docker' }
    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timeout(time: 60, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }
    parameters {
        string(name: 'TEST_CONFIG', defaultValue: 'ci/tests.json',
               description: 'Test plan JSON path in the repository')
        string(name: 'PYVCS_VERSION', defaultValue: 'workspace',
               description: 'workspace or an exact published version, e.g. 0.1.0')
    }
    stages {
        stage('Checkout') {
            steps {
                deleteDir()
                checkout scm
            }
        }
        stage('Integration tests') {
            steps {
                script {
                    def integration = load 'ci/integration.groovy'
                    integration.run(params.TEST_CONFIG, params.PYVCS_VERSION)
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'ci-results/**/*', allowEmptyArchive: true
        }
    }
}
