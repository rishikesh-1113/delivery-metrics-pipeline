pipeline {
    agent any

    environment {
        VENV_DIR   = 'venv'
        DEPLOY_DIR = 'deploy'
    }

    stages {
        stage('Source Checkout') {
            steps {
                checkout scm
                sh '''
                    echo "Workspace: $WORKSPACE"
                    git log -1 --oneline
                    ls -la
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip list
                '''
            }
        }

        stage('Test / Validation') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    python -m pytest -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        stage('Deployment Packaging') {
            steps {
                sh '''
                    rm -rf $DEPLOY_DIR
                    mkdir -p $DEPLOY_DIR
                    cp -r exporter config requirements.txt $DEPLOY_DIR/
                    find $DEPLOY_DIR -name "__pycache__" -prune -exec rm -rf {} +
                    echo "Deployment directory contents:"
                    ls -R $DEPLOY_DIR
                '''
                archiveArtifacts artifacts: 'deploy/**', fingerprint: true
            }
        }
    }

    post {
        success { echo 'BUILD SUCCESS: deployment artifact is ready in deploy/' }
        failure { echo 'BUILD FAILED: check the stage logs above' }
    }
}
