# mytube

mytube is a python script that downloads YouTube videos according to a user-specified
`.yml` file.

## Setup

1. Clone and enter the repository

    ```bash
    git clone https://github.com/zjrubin/mytube.git
    cd mytube
    ```

2. Install the required python packages

    ```bash
    python3 -m pip install -r requirements.txt
    ```

3. Modify `mytube_config.yml` with entries for the videos you'd like to download.

    `NOTE:` You can reference the examples in `mytube_config.yml` to see the format your entries should follow.

4. Run the script!

    ```bash
    python3 mytube.py
    ```
