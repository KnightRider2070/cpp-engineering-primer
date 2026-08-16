# HTTP API

What the browser and your C++ say to each other. Provided by the course; you
never write any of it.

| Method | Path | Body | Returns |
| --- | --- | --- | --- |
| `GET` | `/`, `/app.js`, `/style.css` | — | static files |
| `GET` | `/api/health` | — | `{"ok":true}` |
| `GET` | `/api/state` | — | a Snapshot |
| `POST` | `/api/move` | `{"cell":4}` | a MoveResult |
| `POST` | `/api/reset` | — | a Snapshot |

## Snapshot

```json
{
  "board":  ["x","o","empty","empty","x","empty","empty","empty","empty"],
  "turn":   "o",
  "status": "in_progress",
  "winner": null
}
```

## MoveResult

```json
{
  "ok": false,
  "error": "cell_taken",
  "state": { "board": [...], "turn": "o", "status": "in_progress", "winner": null }
}
```

## How the enums encode

| C++ | JSON |
| --- | --- |
| `Mark::Empty` / `X` / `O` | `"empty"` / `"x"` / `"o"` |
| `Player::X` / `O` | `"x"` / `"o"` |
| `Status::InProgress` / `Won` / `Draw` | `"in_progress"` / `"won"` / `"draw"` |
| `MoveError::None` / `OutOfRange` / `CellTaken` / `GameOver` | `"none"` / `"out_of_range"` / `"cell_taken"` / `"game_over"` |
| empty `std::optional<Player>` | `null` |

Board squares use the string `"empty"` rather than `null`, so every element is
a string and the frontend never needs a null check.

## A refused move is HTTP 200

This surprises people, so it is worth stating plainly.

- **200** — the request was fine, and the game has an answer. That answer may be
  "no, that square is taken". An illegal move is a *game outcome*.
- **400** — the request itself was broken: unparseable JSON, no `cell` field, or
  `cell` is not an integer.

```json
// POST /api/move  {"cell":"middle"}  ->  400
{ "ok": false, "error": "bad_request", "detail": "field 'cell' must be an integer" }
```

That is the same philosophy as "return a result, do not throw", one layer up:
**the transport layer's error model should mirror the domain's.**

## Try it yourself

```bash
./ttt serve      # in one terminal

curl -s localhost:8080/api/state | python3 -m json.tool
curl -s -X POST -H 'Content-Type: application/json' -d '{"cell":4}' \
     localhost:8080/api/move | python3 -m json.tool
curl -i -X POST -H 'Content-Type: application/json' -d '{"cell":99}' \
     localhost:8080/api/move
```

The last one returns **200** with `"error":"out_of_range"`. Reading your own API
with `curl` is a genuinely useful habit.
