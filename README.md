# auto-mining-GUI

A GUI version of auto-miner

## Reminders

- You have to *modify the wallet by your self*. To make things clear there's no single line in the code which interact with your wallet (no reading, no modification, ...)
- Some users suggested that if the miner is closed before a certain amount of time, the risk is that you won't get all the eth you would get if you would have kept the miner on instead. For this reason, a quick fix would be to avoid *"intermittent mining"*: this happens if the "wait_time_active" parameter is too small (e.g. 10 seconds). in fact, if the gas value fluctuates too much, you could face a situation for which the miner starts and stops repeatedly, falling in the situation mentioned above. Practically speaking, I would suggest you to keep a "wait_time_active" parameter high (e.g. 1 hour == 3600 seconds).
- Remember that this script's purpose is to *optimize* your revenue, taking into account also your GPU stress, not to maximize it.

## GUI

- Status: it indicates the status of the miner, not of the script itself. It begins as 'Not running' if the miner is not running and as 'Running' is the miner is currently running.

- 'API status', it indicates whether the API is reachable or not depending on the last call. It begin as 'Waiting', after the first check it'll turn to 'Connected'. If there's any connection problem it's going to indicate the number of attempts of reconnection (at the moment this feature is a bit experimental, I'm monitoring to see if it works as intended).

- 'Force start', force the miner to start, regardless of the gas value.

- 'Force stop', force the miner to stop, regardless of the gas value.

- 'Next check', It indicates how much time is left for the next gas value check

- 'Gas Value', each time a gas value check is performed, this value is updated (Green if is > threshold, Red if is < threshold)

Because the amount of checks needed and because the single threaded functioning of tkinter, the GUI is a little laggy: try not to spam Force starts and Force stops.

Also, currently, *force starts and force stops restart the timers!*


## Config.txt

The script is compatible with lolminer and t-rex. It run properly on Windows only. In this file you are going to find a python dictionary which contains 6 keys:

- *'start_gas_threshold'*, it accepts a numerical value which defines the threshold after which the miner starts.
- *'stop_gas_threshold'*, it accepts a numerical value which defines the threshold after which the miner stops.
- *'wait_time_inactive'*, it accepts a numerical value, which defines how much time the script should wait for each gas value check (in seconds), when miner is OFF.
- *'wait_time_active'*, it accepts a numerical value, which defines how much time the script should wait for each gas value check (in seconds), when miner is ON.
- *API*, it accepts an API token from https://etherscan.io/apis#gastracker, you could try to put 'YourApiKeyToken', but this way you have some time limitations.
- *gas_oracle*, you have 3 options: 'SafeGasPrice', 'ProposeGasPrice', 'FastGasPrice' to choose from.

## logs.txt

Logs have been temporarily removed

## miner's update check feature

This feature has been removed, it worked, but there were a lot of corner cases not covered. Because of this, now you are not obliged to change the dirs structure to make it work properly.

## directory.txt

*Only the first line is read*

At the first run you are going to be asked about the .bat file you want to use. If you ever change your mind, just delete the line within the directory.txt and restart the script (or write it manually).

## requirements.txt

list of required packages
