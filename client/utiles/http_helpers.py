def handle_response(response, success_msg=None, failure_msg=None):
    if response.ok:
        if success_msg:
            print(success_msg)
        return response.json()
    else:
        try:
            error_detail = response.json().get("detail", "No details provided")
        except Exception:
            error_detail = response.text
        print(failure_msg or "Request failed.")
        print(f"Status code: {response.status_code}")
        print(f"Error: {error_detail}")
        return None