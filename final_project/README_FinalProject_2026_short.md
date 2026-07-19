# Final Project — TCP Signal Visualization Application

## Overview

For the final project, you will build a **PySide6 desktop application** for live visualization and offline inspection of streamed signal data.

The application receives data from a TCP server provided by us (Exercise 5). Your task is to build the client application around it.

The project combines the topics from the previous exercises:

| Exercise   | Topic |
|------------|---|
| Exercise 2 | Offline plotting with Matplotlib |
| Exercise 3 | PySide6 GUI basics and signal processing |
| Exercise 4 | Real-time plotting with VisPy and MVVM |
| Exercise 5 | TCP streaming and buffering |

The final application should use **MVVM-style programming** and should be uploaded to GitHub.

---

## Team Information

- The project must be completed in teams of **3 students**.
- Each team member should contribute meaningfully and equally.
- You may divide the work, for example into TCP/backend, visualization/frontend, and documentation/integration. If you choose to do so, please clearly specify each team member’s responsibilities in your README.

---

## Support and Contact

If you have any questions, please use the Q&A sessions held during the exercise timeslots or the StudOn forum as your primary channels of communication so that other students can also benefit from shared answers to similar issues.

In urgent cases, you may contact us via email:

- Daniel Fenzel: daniel.fenzel@fau.de
- Annika Ritter: annika.ritter@fau.de

---

## Submission

Submit your project by sending a GitHub repository link by email. Please also indicate your group number.

Deadline:

```text
31.07. , 24:00
```

Send the link to:

```text
- Daniel Fenzel: daniel.fenzel@fau.de
```
or
```text
- Annika Ritter: annika.ritter@fau.de
```

- The repository must be accessible at the time of the deadline and remain accessible thereafter.
- Late changes after the deadline will not be considered.

---

# Minimum Requirements

## 1. TCP Connection

Your GUI must allow the user to connect to the provided TCP server.

The GUI should include:

- an input field for the TCP port
- a connect button
- a disconnect or stop button
- a visible connection status

After a successful connection, streaming should start automatically.

The server is provided by us. Reuse the one we provided in Exercise 5. Your application only needs to implement the client side.

---

## 2. Data Format

The TCP data format is the same as in Exercise 5.

Each received chunk contains:

```text
32 channels x 18 samples
```

The values are sent as raw bytes.

In the version used in the exercises, the data type is:

```text
float64
```

So one packet contains:

```text
32 x 18 x 8 = 4608 bytes
```

You can refer to Exercise 5 for the TCP client structure, byte buffer, packet reconstruction, and rolling buffer.

---

## 3. Live Plot with VisPy

Incoming data must be visualized live using **VisPy**.

The live plot should include:

- one selected channel at a time
- a rolling time window
- visible x-axis and y-axis
- time labels on the x-axis
- readable y-axis scaling

The user must be able to change the displayed channel.

In addition, the GUI should include a button called **Plot All Channels**.

This button should show all 32 channels at the same time. To make the signals readable, the channels should be plotted with a small vertical offset between them.

Example idea:

```text
Channel 1   ───── signal
Channel 2      ───── signal
Channel 3         ───── signal
...
Channel 32                         ───── signal
```

The purpose of this view is to give a quick overview of the complete recording or live signal activity across all channels.


---

## 4. Signal Modes

The user must be able to switch between:

- original signal
- RMS signal
- filtered signal

These modes are required for both:

- live VisPy visualization
- offline Matplotlib visualization

The RMS and filter implementation can be similar to what was done in the previous exercises, especially Exercise 2.

Document briefly what RMS window and filter parameters you used.

---

## 5. Offline Inspection with Matplotlib

When streaming has stopped or the user disconnects, the user should be able to inspect the received signal offline with **Matplotlib**.

The offline view should allow:

- channel selection
- switching between original, RMS, and filtered signal
- inspection of the recorded signal over time

The offline plot does not need to update live.

---

## 6. MVVM Structure

Use an MVVM-style structure.

This means:

- Views contain the GUI and plotting widgets.
- ViewModels manage application state and connect GUI actions to the data logic.
- Models or services handle TCP communication, buffering, and signal processing.

The View should not directly receive TCP data.

The Model should not contain GUI code.

Example structure:

```text
final_project/
├── main.py
├── README.md
├── requirements.txt
├── models/
├── viewmodels/
└── views/
```

You can use a different structure if the responsibilities are clear.

---

## 7. Error Handling

Your application should handle common problems without crashing.

Examples:

- server is not running
- wrong port entered
- connection is lost
- no data available for offline plotting
- invalid channel or processing selection

A simple status message in the GUI is enough.

Example:

```python
try:
    self.model.connect(port)
except OSError as error:
    self.status_updated.emit(f"Could not connect: {error}")
```

---

## 8. Documentation

Your repository must include a `README.md`.

Specify group name, team members and responsibities, if you split the tasks.

It should explain:

- how to install dependencies
- how to run the application
- how to connect to the TCP server
- how to use the live plot
- how to open the offline plot
- how to switch channels and signal modes
- which RMS and filter parameters are used
- how the project is structured according to MVVM

Also include useful comments or docstrings in the code, especially for:

- TCP receiving
- buffering
- signal processing
- ViewModel communication

---

## 9. Dependencies

Include a dependency file.

Use either:

```text
requirements.txt
```

or, if you use `uv`:

```text
pyproject.toml
```

Typical dependencies are:

```text
numpy
scipy
matplotlib
pyside6
vispy
```

Add any other packages you use.

---

# Pass Criteria

The final project is assessed on a **pass/fail** basis.

To pass the project, the submitted application must meet the following minimum requirements:

- working TCP connection and correct data handling
- real-time signal visualization with VisPy
- channel selection
- original, RMS, and filtered signal modes
- display of all channels at the same time (**Plot All Channels** Button)
- offline signal inspection with Matplotlib
- MVVM-style project structure
- usable and understandable GUI
- basic error handling
- README and useful code documentation
- complete GitHub repository with all required files

Please make sure the application can be set up and run on a clean installation using only the dependencies listed in requirements.txt or pyproject.toml. If the application cannot be installed, launched or runs with critical errors, the remaining criteria cannot be checked and the project will not pass.

---

# Tips

- Start with the TCP client before building advanced GUI features.
- Test early with the provided server.
- Keep the View, ViewModel, and Model responsibilities separated.
- Commit regularly with Git (and use meaningful commit messages).
- Test your setup on a clean environment before submitting — do not assume your requirements.txt is correct without verifying it with a fresh install.

Good luck with your final project!
