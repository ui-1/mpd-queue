# mpd-queue

- - -

A small [Beets](https://github.com/beetbox/beets) plugin to add newly imported tracks to the queue of your [MPD](https://github.com/MusicPlayerDaemon/MPD) server.

## Installation

To install the plugin, simply run the following:
```python
pip install mpd-queue
```
and then add `mpd-queue` to the list of enabled plugins in your Beets config.

## Configuration

Optionally, to specify a non-default location for the MPD server, add a configuration block like this:
```yaml
mpd-queue:
  host: example.com
  port: 6601
```

### Options

| Key  | Description                 | Default value |
|------|-----------------------------|---------------|
| host | Hostname of the MPD server  | localhost     |
| port | Port to use when connecting | 6600          |
