# PushWrap

Pushwrap is a simple wrapper for [simplepush.io](https://simplepush.io) that monitors any CLI command and sends a push notification upon completion (either success or failure). Its similiar to [ntfy](https://github.com/binwiederhier/ntfy), but much less complex and easier to set up. 

## Setup
Generate a key on simplepush.io and create two events: "success" and "error" (you can also define different notification types for each event).
You can pass the key to PushWrap either via `SIMPLEPUSH_KEY env var` or with any command using `--push-key KEY`.

Install the script by saving it to `/usr/local/bin/pushwrap`.
```bash
sudo cp pushwrap.py /usr/bin/local/pushwrap
```
Then make it executable:
```bash
sudo chmod +x /usr/bin/local/pushwrap
```
And it's ready to use.


## Usage
```python
usage: pushwrap [-h] [--push-key PUSH_KEY] [--min-seconds MIN_SECONDS] [--no-push]
                [--title-success TITLE_SUCCESS] [--title-failure TITLE_FAILURE]
                ...

Run any command and send Simplepush notification when finished

positional arguments:
  command               Command to run (use -- before command)

options:
  -h, --help            show this help message and exit
  --push-key PUSH_KEY   Simplepush key (or via SIMPLEPUSH_KEY env var)
  --min-seconds MIN_SECONDS
                        Only send push if runtime >= this value
  --no-push             Disable push (dry wrapper run)
  --title-success TITLE_SUCCESS
                        Push title on success
  --title-failure TITLE_FAILURE
                        Push title on failure
```

For example, get notified when your system update is complete:

```bash
pushwrap --push-key KEY -- sudo pacman -Syyuu
```

The above command generates this push notification:
![success](https://i.ibb.co/5g7pFfKJ/push-success.png)

I mainly use it in the context of lengthy, difficult-to-predict tasks such as password cracking with Hashcat, but it should also work well in any other area.

## Tricks
Create an alias in your bash/zsh environment, so you can call the wrapper more easily. For example:
```bash
p='/LOCATION/pushwrap.py --push-key KEY -- '
```
so you can call the wrapper just with
```bash
p sudo pacman -Syyuu
```
This has the advantage that the wrapper can interact with other aliases in your environment, and you don't have to install `pushwrap.py` to `/usr/local/bin` - but you still have to make it executable with `chmod +x`.