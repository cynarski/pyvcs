def integerInRange(value, int minimum, int maximum, String field) {
    if (!(value instanceof Integer) || value < minimum || value > maximum) {
        error("${field} must be an integer from ${minimum} to ${maximum}")
    }
    return value
}

def run(String configPath, String version) {
    if (!(configPath ==~ /[A-Za-z0-9_\/.\-]+\.json/) ||
            configPath.startsWith('/') || configPath.tokenize('/').contains('..')) {
        error('TEST_CONFIG must be a relative JSON path inside the repository')
    }
    if (version != 'workspace' && !(version ==~ /[0-9][A-Za-z0-9.!+\-]*/)) {
        error('PYVCS_VERSION must be workspace or an exact package version')
    }
    def config = readJSON(file: configPath, returnPojo: true)
    if (!(config instanceof Map)) {
        error('The test plan must be a JSON object')
    }
    int workers = integerInRange(config.containers, 1, 32, 'containers')
    int minutes = integerInRange(config.timeout_minutes, 1, 50, 'timeout_minutes')
    if (!(config.tests instanceof List) || config.tests.isEmpty()) {
        error('tests must be a nonempty list')
    }
    def jobs = []
    config.tests.each { test ->
        if (!(test instanceof Map) || !(test.nodeid instanceof String) ||
                !(test.nodeid ==~ /tests\/integration\/[A-Za-z0-9_\/]+\.py::test_[A-Za-z0-9_]+/)) {
            error('Each nodeid must select one test function in tests/integration')
        }
        int repeat = integerInRange(test.repeat, 1, 100, 'repeat')
        for (int i = 0; i < repeat; i++) {
            jobs.add([id: jobs.size() + 1, nodeid: test.nodeid])
        }
        if (jobs.size() > 1000) {
            error('At most 1000 test executions are allowed')
        }
    }
    if (workers > jobs.size()) {
        error('containers cannot exceed the number of test executions')
    }
    def shards = (0..<workers).collect { [] }
    for (int i = 0; i < jobs.size(); i++) {
        shards[i % workers].add(jobs[i])
    }
    def token = sh(script: 'mktemp -d ci-run-XXXXXXXXXX', returnStdout: true).trim().toLowerCase()
    def image = "pyvcs-ci:${token}"
    sh 'mkdir -p ci-results'
    writeJSON(file: 'ci-results/plan.json', json: [
        version: version, containers: workers, jobs: jobs
    ], pretty: 2)
    echo "Running ${jobs.size()} test executions in ${workers} containers"
    try {
        withEnv(["CI_IMAGE=${image}", "CI_PYVCS_VERSION=${version}"]) {
            sh 'docker build --build-arg "PYVCS_VERSION=$CI_PYVCS_VERSION" -f ci/Dockerfile -t "$CI_IMAGE" .'
        }
        def branches = [:]
        for (int i = 0; i < workers; i++) {
            int worker = i
            def batch = shards[i]
            branches["worker-${worker + 1}"] = {
                timeout(time: minutes, unit: 'MINUTES') {
                    runWorker(image, "${token}-${worker + 1}", worker + 1, batch)
                }
            }
        }
        parallel branches
    } finally {
        for (int i = 1; i <= workers; i++) {
            withEnv(["CI_CONTAINER=${token}-${i}"]) {
                sh(script: 'docker rm -f "$CI_CONTAINER" >/dev/null 2>&1 || true', returnStatus: true)
            }
        }
        withEnv(["CI_IMAGE=${image}"]) {
            sh(script: 'docker image rm "$CI_IMAGE" >/dev/null 2>&1 || true', returnStatus: true)
        }
    }
}

def runWorker(String image, String container, int worker, List jobs) {
    def output = "ci-results/worker-${worker}"
    withEnv(["CI_IMAGE=${image}", "CI_CONTAINER=${container}", "CI_OUTPUT=${output}"]) {
        sh 'mkdir -p "$CI_OUTPUT"'
        writeJSON(file: "${output}/jobs.json", json: jobs, pretty: 2)
        try {
            sh 'docker create --name "$CI_CONTAINER" "$CI_IMAGE"'
            sh 'docker cp "$CI_OUTPUT/jobs.json" "$CI_CONTAINER:/suite/jobs.json"'
            int status = sh(script: 'docker start -a "$CI_CONTAINER"', returnStatus: true)
            sh 'docker cp "$CI_CONTAINER:/results/." "$CI_OUTPUT/"'
            junit testResults: "${output}/run-*.xml", allowEmptyResults: false
            if (status != 0) {
                error("Worker ${worker} failed with exit code ${status}; see its reports")
            }
        } finally {
            // Preserve partial reports on timeout or infrastructure failure.
            sh(script: 'docker cp "$CI_CONTAINER:/results/." "$CI_OUTPUT/"', returnStatus: true)
            sh(script: 'docker rm -f "$CI_CONTAINER"', returnStatus: true)
        }
    }
}

return this
