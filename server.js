
const express = require('express');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync, exec } = require('child_process');
const cors = require('cors');

const app = express();

app.use(express.json());
app.use(cors());

app.use((req, res, next) => {
    console.log(req.method, req.url);
    next();
})

const PORT = 3000;

function runTestCase(exePath, input, expectedOutput, timeLimit, memLimit) {
    return new Promise((resolve) => {
        const start = Date.now();
        const tmpIn = path.join(os.tmpdir(), `in_${Date.now()}`);
        fs.writeFileSync(tmpIn, input);

        const memKB = memLimit * 1024;
        const cmd = `bash -c "ulimit -v ${memKB}; timeout ${timeLimit} ${exePath} < ${tmpIn}"`;

        exec(cmd, { timeout: (timeLimit + 2) * 1000 }, (err, stdout, stderr) => {
            fs.unlinkSync(tmpIn);
            const elapsed = Date.now() - start;

            if (err?.code === 124 || elapsed >= timeLimit * 1000) return resolve({ status: 'TLE', elapsed, stdout: '' });
            if (err?.code === 137 || stderr.includes('Killed')) return resolve({ status: 'MLE', elapsed, stdout: '' });
            if (err) return resolve({ status: 'RE', stdout: '', stderr: stderr.slice(0, 300) });

            const actual = stdout.trimEnd();
            const expected = expectedOutput.trimEnd();
            resolve(actual === expected ? { status: 'AC', elapsed, stdout: actual } : { status: 'WA', elapsed, stdout: actual, expected });
        });
    });
}

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.post('/judge', async (req, res) => {
    const { code, testCases, timeLimit = 2, memLimit = 256 } = req.body;

    const codeDir = fs.mkdtempSync(path.join(os.tmpdir(), 'judje_'));
    const codePath = path.join(codeDir, 'solution.cpp');
    const exePath = path.join(codeDir, 'solution');

    fs.writeFileSync(codePath, code);

    try {
        execSync(`g++ -O2 -std=c++17 -o ${exePath} ${codePath}`, {
            timeout: 10000,
            stdio: 'pipe',
        });
    } catch (e) {
        console.log('Compile erorr: ', e.message);
        fs.rmSync(codeDir, { recursive: true });
        return res.json({ erorr: 'CE', message: e.stderr.toString() });
    }

    const results = [];
    for (let i = 0; i < testCases.length; i++) {
        const input = { input, output } = testCases[i];
        const result = await runTestCase(execPath, input, output, timeLimit, memLimit);
        results.push({ index: i + 1, ...result });
    }

    fs.rmSync(codeDir);
    res.json({ results });
});

app.listen(PORT, () => console.log('App is running on port 3000!!!!'));