# Theme System

The `THEME` block allows you to attach lightweight visual styling metadata to a quiz. Themes do not affect quiz logic — they provide hints to renderers and exporters about how the quiz should be displayed.

---

## Syntax

```
THEME {
    background = dark
    font       = Georgia
    question   [font=Arial, size=18]
    correct    [color=green]
    wrong      [color=red]
}
```

Top-level properties apply globally. Selector blocks apply styles to specific parts of the quiz.

---

## Global Properties

These properties apply to the quiz as a whole:

| Property     | Description                              | Example values          |
|--------------|------------------------------------------|-------------------------|
| `background` | Background color or theme name           | `dark`, `light`, `#fff` |
| `foreground` | Default text color                       | `#333`, `white`         |
| `accent`     | Highlight or interactive color           | `blue`, `#ff6600`       |
| `font`       | Default font family                      | `Georgia`, `monospace`  |
| `spacing`    | Global spacing scale                     | `compact`, `relaxed`    |
| `radius`     | Corner radius for UI elements            | `4px`, `none`, `full`   |

---

## Selectors

Selector blocks apply scoped styles to specific parts of the rendered quiz:

| Selector   | Applies to                          |
|------------|-------------------------------------|
| `quiz`     | The overall quiz container          |
| `question` | Question text and question blocks   |
| `answer`   | All answer options                  |
| `correct`  | Answers marked as correct           |
| `wrong`    | Answers marked as incorrect         |

---

## Selector Attributes

The following attributes can be used inside any selector block:

| Attribute  | Description              | Example          |
|------------|--------------------------|------------------|
| `font`     | Font family              | `font=Arial`     |
| `size`     | Font size (in px or pt)  | `size=18`        |
| `color`    | Text color               | `color=green`    |
| `weight`   | Font weight              | `weight=bold`    |
| `spacing`  | Element spacing          | `spacing=loose`  |

---

## Full Example

```
THEME {
    background = dark
    foreground = #f0f0f0
    accent     = #00bcd4
    font       = Georgia
    radius     = 8px

    question [font=Arial, size=20, weight=bold]
    answer   [size=16]
    correct  [color=green]
    wrong    [color=red]
}
```