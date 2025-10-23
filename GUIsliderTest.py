#Code from ChatGPT 5

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QCheckBox
)
from PyQt5.QtCore import Qt


class EffectControlPanel(QWidget):
    def __init__(self, effects):
        super().__init__()
        self.setWindowTitle("Effect Control Panel")
        self.effects = effects
        self.effect_controls = {}  # store widgets for later access

        # main layout
        main_layout = QVBoxLayout()

        for effect in self.effects:
            row_layout = QHBoxLayout()

            # Checkbox (on/off)
            checkbox = QCheckBox(effect)
            checkbox.setChecked(False)

            # Slider (intensity)
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(100)
            slider.setValue(50)
            slider.setTickPosition(QSlider.TicksBelow)
            slider.setTickInterval(10)

            # Label to show value
            value_label = QLabel("50")

            # Connect slider signal to update label
            slider.valueChanged.connect(lambda val, lbl=value_label: lbl.setText(str(val)))

            # Add to layout
            row_layout.addWidget(checkbox)
            row_layout.addWidget(slider)
            row_layout.addWidget(value_label)

            main_layout.addLayout(row_layout)

            # Keep references to widgets for each effect
            self.effect_controls[effect] = {
                "checkbox": checkbox,
                "slider": slider,
                "label": value_label
            }

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    effects = ["Blur", "Sharpen", "Edge Detection", "Brightness", "Contrast"]
    window = EffectControlPanel(effects)
    window.resize(500, 200)
    window.show()
    sys.exit(app.exec_())
