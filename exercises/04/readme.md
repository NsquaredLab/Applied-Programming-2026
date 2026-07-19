# Exercise 4 — Real-Time Plotting with VisPy and MVVM

## Overview

In this exercise, you will build a small desktop application for **real-time signal visualization** using:

- **PySide6** for the application window
- **VisPy** for fast real-time plotting
- **MVVM** (Model-View-ViewModel) for code structure

This exercise is an important bridge between the earlier PySide6 UI exercise and the final project.

Here, the signal is still simulated locally. Later, in the final project, the same structure can be reused with TCP data instead of generated data.

---

## Why this exercise matters

In earlier exercises, you worked with:

- loading and processing signals
- plotting offline data with Matplotlib
- building a basic UI with PySide6

Now you combine these ideas into a **small real-time application**.

That means you are no longer just writing a script that runs once and stops.

Instead, you are building an application that:

- stays open
- reacts to user input
- updates continuously
- separates responsibilities across multiple files

That is much closer to how real software systems are built.

---

## Learning Goals

By the end of this exercise, you should understand:

- why **VisPy** is better suited than Matplotlib for live plotting
- how a **sliding window** visualization works
- how to structure code using **MVVM**
- how data flows from a Model to a View through a ViewModel
- how a Qt timer drives repeated updates
- how **signals and slots** enable communication without tightly coupling components
- how this structure can later be extended to TCP-based live data

---

# Part 1 — Why VisPy?

## Matplotlib vs VisPy

Matplotlib is excellent for:

- static figures
- offline analysis
- publication-quality plots
- signal inspection after processing

But live plotting is a different use case.

If you update a Matplotlib figure many times per second, it quickly becomes less efficient because the figure is repeatedly redrawn in a relatively heavy plotting system.

**VisPy** is designed for high-performance visualization and uses GPU acceleration.

That makes it much more suitable for:

- real-time signal displays
- smooth updates
- interactive views
- continuously changing data

So the decision here is not:

> “Which library is better in general?”

It is:

> “Which library is better for this task?”

For this task — real-time plotting — the answer is **VisPy**.

---

# Part 2 — What does “real-time plotting” mean here?

The signal in this exercise is not actually coming from hardware yet.

It is generated in software.

But the app behaves **as if** data were arriving over time.

That is what makes this a good preparation for the final project.

---

## Sliding window visualization

The entire signal exists as one long time series.

Instead of displaying the whole signal at once, we display only a **window**:

- `window_size` = how many samples are visible
- `step_size` = how far the window moves at each update

Example:

```text
first frame:  samples 0    : 5000
next frame:   samples 20   : 5020
next frame:   samples 40   : 5040
next frame:   samples 60   : 5060
```

This creates the impression of a moving, continuously updating signal.

---

## Why use a window?

Because in real-time systems:

- you usually care most about the **most recent data**
- plotting the full history all the time is inefficient
- a window is easier to read visually

This is exactly the same idea you will need later when data arrives over TCP.

---

# Part 3 — MVVM in detail

This is the most important concept in the exercise.

## Why not put everything into one file?

You *could* make one file that:

- creates the signal
- handles the button
- owns the timer
- updates the plot
- builds the UI

But that becomes messy quickly.

Problems with that approach:

- hard to debug
- hard to extend
- hard to test
- hard to reuse

Most importantly:

- the UI becomes tightly coupled to the data logic
- changing one thing often breaks several others

That is why we use **MVVM**.

---

## What is MVVM?

MVVM stands for:

- **Model**
- **View**
- **ViewModel**

It is a way to separate responsibilities.

---

## Model

The Model owns the **data**.

It answers questions like:

- What signal are we using?
- How is it stored?
- What data window should be returned?

It should **not** care about:

- buttons
- labels
- window layout
- plotting widgets
- timer state

The Model should not know that a graphical user interface exists.

Its role is only:

> “Here is the data you asked for.”

---

## View

The View owns the **user interface**.

It answers questions like:

- What widgets exist?
- What does the user see?
- What happens when a button is clicked?
- How should the plot be displayed?

It should **not** implement:

- data generation
- signal processing logic
- timer/state logic
- sliding-window logic

The View is allowed to update presentation details, for example:

- button text
- label text
- plot visuals

But it should not decide which signal window comes next. That belongs to the ViewModel.

---

## ViewModel

The ViewModel sits between Model and View.

It answers questions like:

- Are we currently plotting?
- Which data window should be shown next?
- When should the next update happen?
- What data should be sent to the View?

The ViewModel connects:

- **Model → data**
- **View → interaction**

So the ViewModel is the layer where application logic lives.

---

## Simple mental model

Think of it like this:

### Model

> “I own the signal.”

### ViewModel

> “I decide what part of the signal is shown, and when.”

### View

> “I display what I receive and forward button clicks.”

---

## MVVM in this exercise

| MVVM part | File | Responsibility |
|---|---|---|
| Model | `models/signal_model.py` | Creates/stores the signal and returns data windows |
| ViewModel | `viewmodels/mainViewModel.py` | Owns timer, current index, plotting state, and emits new data |
| View | `views/mainView.py` | Builds the main UI, handles button clicks, connects signals |
| View | `views/plotView.py` | Displays the signal using VisPy |
| App entry point | `main.py` | Creates the application, ViewModel, and View |

---

## Important MVVM rule for this exercise

Use this rule when deciding where code belongs:

- If it creates or stores signal data → **Model**
- If it decides what should happen next → **ViewModel**
- If it displays something or reacts to a button click → **View**

Examples:

| Task | Correct place |
|---|---|
| Generate the simulated signal | Model |
| Return samples `current_index : current_index + window_size` | Model |
| Remember whether plotting is active | ViewModel |
| Start and stop the timer | ViewModel |
| Emit new plot data | ViewModel |
| Change button text | View |
| Draw the line with VisPy | View |

---

## Data flow in MVVM

The data flow in this exercise is:

1. User clicks **Start Plotting**
2. View calls a method that interacts with the ViewModel
3. ViewModel starts a timer
4. Timer triggers repeated updates
5. ViewModel asks Model for the next window
6. ViewModel emits the new data
7. View receives the data and updates the plot

So the View does **not** go directly to the Model.

That is one of the most important MVVM rules:

> The View should not directly fetch or manipulate model data.

Instead, it should work through the ViewModel.

---

## Data flow with actual method names

In this exercise, the flow looks like this:

```text
toggle_button.clicked
        ↓
MainView.toggle_plotting()
        ↓
MainViewModel.start_plotting()
        ↓
QTimer.timeout
        ↓
MainViewModel.update_plot()
        ↓
SignalModel.get_window(current_index)
        ↓
MainViewModel.plot_updated.emit(x, y)
        ↓
VisPyPlotWidget.update_plot(x, y)
```

This is the central communication path of the application.

---

## Wrong vs. better MVVM example

### Wrong: View directly asks the Model for data

```python
x, y = self.model.get_window(0)
self.plot_widget.update_plot(x, y)
```

This couples the user interface directly to the data source.

If the data source later changes from a simulated signal to TCP data, the View may also need to change.

---

### Better: View talks to the ViewModel

```python
self.view_model.start_plotting()
```

The ViewModel decides when to request data from the Model and emits the result to the View.

The View does not need to know where the data comes from.

---

## Why this helps in the final project

Later, your Model may no longer generate a fake signal.

Instead, it may:

- store TCP data
- buffer incoming packets
- provide multi-channel chunks

If your architecture is clean, you can swap the Model without rewriting everything else.

That is one of the major benefits of MVVM:

- **better scalability**
- **easier replacement of components**
- **cleaner extension paths**

---

# Part 4 — Folder Structure

Your files are organized like this:

```text
exercise_04/
├── main.py
├── models/
│   ├── __init__.py
│   └── signal_model.py
├── views/
│   ├── __init__.py
│   ├── mainView.py
│   └── plotView.py
├── viewmodels/
│   ├── __init__.py
│   └── mainViewModel.py
└── README.md
```

---

## Why split into folders?

This helps you see immediately:

- where UI code belongs
- where logic belongs
- where data code belongs

It also mirrors the final project structure more closely.

The `__init__.py` files are needed so Python treats the folders as importable packages.

---

# Part 5 — File-by-file explanation and TODO guidance

## `main.py`

### What this file does

This file is the **entry point** of the application.

Its job is to:

- create the Qt application
- create the ViewModel
- create the View
- connect them through construction
- show the main window
- start the event loop

### Why is this file small?

Because `main.py` should only assemble the application.

It should **not** contain business logic.

A good `main.py` is usually very small.

---

### Typical startup pattern

A Qt application usually starts with:

```python
app = QApplication(sys.argv)
```

Then you create your objects:

```python
view_model = ...
view = ...
```

Then display the window:

```python
view.show()
```

And finally start the event loop:

```python
app.exec()
```

---

### TODO guidance for `main.py`

The TODOs here are intentionally light.

They reinforce the architecture:

- create the **ViewModel first**
- pass it into the **View**
- show the View

### Why ViewModel first?

Because the View depends on it.

The View needs a ready-to-use ViewModel object so it can:

- connect to signals
- call start/stop methods
- check state

This is a small but important architectural lesson:

- dependencies should be explicit
- objects should receive what they need

---

## `models/signal_model.py`

### What this file does

This is the **Model**.

Its job is to:

- create or store the signal
- know the sampling rate
- return windows of data
- check whether enough data remains for another window

### Why is this called a Model?

Because it owns the underlying data and does not care about the UI.

It should not know:

- whether there is a button
- whether plotting is active
- whether the user pressed Start

Its role is only:

> “Here is the data you asked for.”

---

### `get_window(start_idx)`

This method returns one time window of data.

Conceptually:

```text
full signal → choose one segment → return x and y
```

The ViewModel will call this repeatedly as the window moves.

---

### `has_enough_data(start_idx)`

This method checks whether a full window can still be extracted.

Why is that useful?

Because if the requested start index is too close to the end, then:

- a full window would no longer fit
- array shapes could become inconsistent
- the animation logic becomes messy

So the ViewModel uses this method to decide whether it should reset to the beginning.

---

## `viewmodels/mainViewModel.py`

This is the most important file conceptually.

It contains the logic that turns a static signal into a time-based animation.

### Responsibilities of the ViewModel

- create the Model
- store plotting state
- store current position in the signal
- create and manage a timer
- request the next data window
- emit plot data for the View

---

### `QObject`

The ViewModel inherits from `QObject` because it needs Qt features such as:

- `Signal`
- timer integration
- event-based behavior

So the ViewModel is not just a plain Python class.

It participates in the Qt signal-slot system.

---

### `Signal(object, object)`

The signal

```python
plot_updated = Signal(object, object)
```

means:

> “This ViewModel can emit two Python objects.”

In this exercise, those two objects are:

- `x`
- `y`

That is how the ViewModel sends new plot data to the View without directly touching the plot internals.

---

### Why emit instead of directly plotting?

Because in MVVM:

- the ViewModel should not control drawing details
- the View should stay responsible for presentation

So instead of doing this inside the ViewModel:

```python
self.plot_widget.set_data(...)
```

the ViewModel emits data, and the View decides how to display it.

That is cleaner and more reusable.

---

### `QTimer`

The timer is what makes the plot update repeatedly.

A timer emits a signal after a specified interval.

Example idea:

- every 10 ms
- call `update_plot()`

This is much better than a loop like:

```python
while True:
    ...
```

Why?

Because a normal loop would block the GUI and freeze the window.

`QTimer` works *with* the Qt event loop, not against it.

---

### TODO guidance in `mainViewModel.py`

#### Creating the Model

The ViewModel should create the Model object once during initialization.

Why?

Because the ViewModel needs a source of data for all later updates.

Expected idea:

```python
self.model = SignalModel(
    sampling_rate=1000,
    duration=100,
    window_size=5000,
    step_size=20,
)
```

---

#### Storing state

The ViewModel needs state variables such as:

```python
self.current_index = 0
self.is_plotting = False
```

Why?

Because someone needs to remember:

- where the current window starts
- whether the timer should be running

That “someone” is the ViewModel.

---

#### Creating the timer

The ViewModel should create a `QTimer` and connect its timeout signal to `update_plot`.

Expected idea:

```python
self.timer = QTimer(self)
self.timer.timeout.connect(self.update_plot)
```

This means:

> each timer tick causes one new plotting update

That is the core mechanism for the animation.

---

#### Starting plotting

When plotting starts, the ViewModel should:

- check whether plotting is already running
- update its state
- start the timer

This is an example of a **guard condition**.

A guard condition prevents invalid transitions, such as starting the timer twice.

Expected idea:

```python
if not self.is_plotting:
    self.is_plotting = True
    self.timer.start(10)
```

---

#### Stopping plotting

Similarly, when stopping:

- check whether plotting is currently running
- update state
- stop the timer

Expected idea:

```python
if self.is_plotting:
    self.is_plotting = False
    self.timer.stop()
```

Again, guard conditions keep the state consistent.

---

### Why we did not leave `update_plot()` as a TODO

That method contains the core sliding-window logic, and it becomes harder quickly if too many parts are removed at once.

So in this exercise, the focus is on:

- timer setup
- state ownership
- signal emission logic

without making you debug too much infrastructure at the same time.

Before `update_plot()` can work, `self.model` must contain a `SignalModel` object and `self.current_index` must be an integer.

---

## `views/plotView.py`

This file is the VisPy-specific visualization component.

It is a **View**, but a specialized one:

- it does not manage the whole window
- it only manages the plot area

---

### What this file teaches

- how VisPy organizes a plotting scene
- how a line visual is updated
- how axis widgets are linked to a view
- how to update camera range dynamically

---

### SceneCanvas

The `SceneCanvas` is the VisPy drawing surface.

It plays a role similar to:

- a canvas
- a rendering area
- a visualization surface

But unlike a Matplotlib figure, it is optimized for faster updates.

---

### Grid inside the SceneCanvas

VisPy uses its own scene/widget system.

The grid is used to organize:

- y-axis
- plot view
- x-axis

This is not the same as a Qt layout.

It is part of VisPy’s own internal scene organization.

---

### View vs Widget

This distinction is important.

- A Qt `QWidget` is a GUI container
- A VisPy `View` is the actual plotting scene

So when you see:

```python
self.view = ...
```

that is not the same kind of object as the outer Qt widget.

---

### Axis widgets

Axis widgets show:

- ticks
- axis lines
- scale reference

But they must be linked to the same plotting view so they follow the same camera.

That is why the order matters.

---

### Important constraint: common scenegraph path

Axis widgets and the plotting view must belong to the same VisPy grid structure before linking.

If not, VisPy cannot determine the transformations correctly and runtime errors appear.

That is why this README explains the idea, even if the TODOs do not require you to build the full scene setup from scratch.

---

### Line visual

The line visual is the actual plotted signal.

It is created once, then updated many times.

This is a very important real-time plotting idea:

> Do not recreate the whole plot every frame.
> Create the visual once and update its data.

That is much more efficient.

---

### `update_plot(x, y)`

This method receives new plotting data.

The important ideas inside are:

#### Convert to arrays

This makes sure the data has a clean numeric format.

#### Combine x and y into positions

VisPy expects point data in the form:

```text
(N, 2)
```

meaning:

- one row per point
- column 1 = x
- column 2 = y

For example:

```text
x = [0.00, 0.01, 0.02]
y = [0.10, 0.15, 0.09]
```

should become:

```text
pos = [
    [0.00, 0.10],
    [0.01, 0.15],
    [0.02, 0.09],
]
```

In NumPy, this can be done with:

```python
pos = np.column_stack((x, y))
```

#### Update the line

The line visual should receive the new position array.

#### Update the camera range

If the visible range is not updated, the data might be:

- clipped
- too small
- outside the visible area

Padding is useful so the line is not drawn directly at the border.

---

### Why the TODOs are in `update_plot()`

This is the most concrete part of the VisPy exercise:

- data shape
- plot update
- visible region

These are the ideas you really need to touch yourself.

---

## `views/mainView.py`

This is the main application window.

It is the place where:

- widgets are arranged
- user interaction is handled
- ViewModel signals are connected to visible behavior

Since you already practiced PySide6 UI basics earlier, the focus here is not on layout construction itself, but on **MVVM communication**.

---

### Responsibilities of the MainView

- hold a reference to the ViewModel
- contain the plot widget
- contain the button and label
- forward button clicks
- react to ViewModel signals

---

### Storing the ViewModel

The View needs the ViewModel because it must:

- ask it to start/stop plotting
- check current plotting state
- connect its signals

That is why the View receives the ViewModel in `__init__`.

This is dependency injection in a very simple form:

- the View does not create the ViewModel itself
- it receives it from outside

That makes the structure cleaner.

Expected idea:

```python
self.view_model = view_model
```

---

### Connecting the button

The button click should not directly manipulate timers or model data.

Instead, the button should trigger logic that eventually calls ViewModel methods.

That is a central MVVM idea:

> user actions are forwarded to the ViewModel

Expected idea:

```python
self.toggle_button.clicked.connect(self.toggle_plotting)
```

---

### Connecting `plot_updated`

The ViewModel emits plot data.

The View should connect that signal to the plotting widget.

Expected idea:

```python
self.view_model.plot_updated.connect(self.plot_widget.update_plot)
```

This means the View acts as the layer that wires together:

- data updates from logic
- visual updates in the UI

---

### `toggle_plotting()`

This method is where the View translates user interaction into ViewModel actions.

It should:

- check whether plotting is active
- call `start_plotting()` or `stop_plotting()`
- update the button text
- update the label text

This is a good example of what the View *is* allowed to do:

- reflect state in the UI

But it should not:

- generate data
- manage the timer directly
- compute windows

Those belong elsewhere.

---

# Part 6 — Signals and Slots in detail

This is one of the core Qt concepts.

## What is a signal?

A signal is:

> “Something happened.”

Examples:

- button clicked
- timer timeout
- custom plot data available

---

## What is a slot?

A slot is:

> “A function that reacts to that event.”

---

## Example 1 — Button click

```python
self.toggle_button.clicked.connect(self.toggle_plotting)
```

Meaning:

- signal = `clicked`
- slot = `toggle_plotting`

When the user clicks the button, the function runs.

---

## Example 2 — Timer timeout

```python
self.timer.timeout.connect(self.update_plot)
```

Meaning:

- signal = `timeout`
- slot = `update_plot`

Every timer interval, the update function runs.

---

## Example 3 — Custom signal from ViewModel

```python
plot_updated = Signal(object, object)
```

This defines a custom signal.

Later:

```python
self.plot_updated.emit(x, y)
```

This sends two objects outward.

And then the View connects:

```python
self.view_model.plot_updated.connect(self.plot_widget.update_plot)
```

So the plot widget receives the new data.

---

## Why signals and slots are useful

Without them, you would often end up with:

- direct dependencies everywhere
- hard-coded object references
- messy control flow

Signals and slots help keep components loosely coupled.

That matters a lot in larger applications.

---

# Part 7 — Common Mistakes

## 1. Using `while True` instead of `QTimer`

This usually freezes the UI because the Qt event loop cannot process repaint and interaction events properly.

Use `QTimer` instead.

---

## 2. Recreating the plot object every update

That is inefficient.

Better:

- create the line visual once
- only update its data

---

## 3. Wrong data shape in VisPy

VisPy expects positions shaped like:

```text
(N, 2)
```

If x and y are not combined properly, the plot will fail or look wrong.

---

## 4. Linking axis widgets incorrectly

Axes and plot view must share the same scenegraph context.

If linked incorrectly, runtime errors appear.

---

## 5. Letting the View talk directly to the Model

This breaks MVVM and makes the architecture harder to maintain.

Always route UI actions through the ViewModel.

---

## 6. Putting timer logic into the View

The View may contain buttons and labels, but it should not own the timer.

The timer controls application behavior, so it belongs in the ViewModel.

---

## 7. Forgetting to connect signals

If the app opens but nothing updates, check the signal connections:

- button click connected?
- timer timeout connected?
- ViewModel signal connected to plot widget?

---

# Part 8 — Mini checkpoint before running

Before running the app, check:

- Does `main.py` create the ViewModel before the View?
- Does the View receive the ViewModel as an argument?
- Does the View store the ViewModel in `self.view_model`?
- Does the View connect the button to `toggle_plotting()`?
- Does the View connect `plot_updated` to `update_plot()`?
- Does the ViewModel create a `SignalModel`?
- Does the ViewModel initialize `current_index` with `0`?
- Does the ViewModel initialize `is_plotting` with `False`?
- Does the ViewModel create and connect the `QTimer`?
- Does the plot widget convert `x` and `y` into an `(N, 2)` array?

---

# Part 9 — How this connects to the final project

This exercise already gives you several building blocks that will appear again later.

| This exercise | Final project |
|---|---|
| simulated signal model | TCP-backed signal model |
| single signal | possibly multi-channel signal data |
| QTimer-based updates | live network-driven updates or buffered updates |
| VisPy line plot | multi-channel live visualization |
| MVVM structure | required architecture |
| ViewModel signal emission | data propagation from backend to UI |

So although this exercise uses simulated data, the architecture is already very relevant to the final project.

The most important idea is:

> If the architecture is clean now, replacing the simulated signal with real TCP data later becomes much easier.

---

# Part 10 — How to run

Install dependencies:

```bash
uv add pyside6 vispy numpy
```

Then run:

```bash
python main.py
```

Make sure the files are placed in the correct folders:

- `models/signal_model.py`
- `views/mainView.py`
- `views/plotView.py`
- `viewmodels/mainViewModel.py`

Also ensure these folders contain `__init__.py` files so Python treats them as packages.

---

# Final Takeaway

This exercise is not just about plotting a moving line.

It is about learning how to build a **structured, real-time application** where:

- the **Model** owns the data
- the **ViewModel** owns logic and state
- the **View** owns presentation

That separation is one of the most important habits you can build before starting the final project.
