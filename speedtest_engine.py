#speedtest_engine.py
import speedtest as sp

def run_speed_test():
    try:
        st = sp.Speedtest()
        st.get_best_server()

        # Obs: Results are in bps
        download_speed = st.download()
        upload_speed = st.upload()
        ping = st.results.ping

        return{
            "download": download_speed,
            "upload": upload_speed,
            "ping": ping,
            "isp": st.results.client.get('isp','unknown'),
            "server": st.results.server.get('sponsor', 'Unknown'),
            "location": st.results.server.get('name', 'Unknown'),
        }
    except Exception as e:
        return {
            "error": str(e)
        }