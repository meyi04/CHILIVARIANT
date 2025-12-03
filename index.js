const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { PythonShell } = require('python-shell');

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.get('/', (req, res) => {
    res.send("CHILIVAR-PREDICT NODE API is running!");
});

app.post('/predict', (req, res) => {
    const options = {
        mode: 'json',
        pythonOptions: ['-u'],
        scriptPath: './python'
    };

    const pyshell = new PythonShell('predict.py', options);

    // Send JSON object directly (NOT string)
    pyshell.send(req.body);

    pyshell.on('message', (result) => {
        res.json(result);
    });

    pyshell.end((err) => {
        if (err) {
            res.status(500).json({ error: err.toString() });
        }
    });
});

app.listen(5000, () => {
    console.log("Backend running on port 5000");
});
