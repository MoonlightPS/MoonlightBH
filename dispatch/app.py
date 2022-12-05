from bottle import route, run, request, Bottle


app = Bottle()


@app.route('/')
def running():
    return "Running on MoonlightBH"


ACCOUNT_INFO = {
    "retcode": 0,
    "message": "OK",
    "data": {
        "account": {
            "uid": "1",
            "name": "MoonlightBH",
            "email": "MoonlightBH",
            "mobile": "420****69",
            "is_email_verify": "0",
            "realname": "",
            "identity_card": "",
            "token": "token",
            "safe_mobile": "",
            "facebook_name": "",
            "google_name": "",
            "twitter_name": "",
            "game_center_name": "",
            "apple_name": "",
            "sony_name": "",
            "tap_name": "",
            "country": "CN",
            "reactivate_ticket": "",
            "area_code": " * *",
            "device_grant_ticket": "",
            "steam_name": ""
        },
        "device_grant_required": False,
        "safe_moblie_required": False,
        "realperson_required": False,
        "reactivate_required": False,
        "realname_operation": "None"
    }
}

# Auth Handlers


@app.route("/bh3_usa/mdk/shield/api/login", method="POST")
def route_mdk_shield_api_login():
    return ACCOUNT_INFO


@app.route("/bh3_usa/mdk/shield/api/verify", method="POST")
def route_mdk_shield_api_verify():
    return ACCOUNT_INFO


@app.route("/account/risky/api/check", method="POST")
def route_risky_api_check():
    return {
        "retcode": 0,
        "message": "OK",
        "data": {
            "id": "",
            "action": "ACTION_NONE",
            "geetest": None
        }
    }


@app.route("/bh3_usa/combo/granter/login/v2/login", method="POST")
def route_login_v2():
    return {
        "message": "OK",
        "retcode": 0,
        "data": {
            "account_type": 1,
            "combo_id": 0,
            "combo_token": "token",
            "data": {
                "guest": False
            },
            "fatigue_remind": None,
            "heartbeat": "False",
            "open_id": 1
        }
    }

# Config Handlers


@app.route("/bh3_usa/combo/granter/api/compareProtocolVersion", method="POST")
def compareProtocolVersion():
    return {
        "retcode": 0,
        "message": "OK",
        "data": {
            "modified": True,
            "protocol": {
                "id": 0,
                "app_id": 7,
                "language": "en",
                "user_proto": "",
                "priv_proto": "",
                "major": 0,
                "minimum": 4,
                "create_time": "0",
                "teenager_proto": "",
                "third_proto": ""
            }
        }
    }


@app.route("/bh3_usa/mdk/shield/api/loadConfig")
def route_mdk_shield_api_loadConfig():
    return {
        "retcode": 0,
        "message": "OK",
        "data": {
            "id": 12,
            "game_key": "bh3_usa",
            "client": "PC",
            "identity": "I_IDENTITY",
            "guest": False,
            "ignore_versions": "",
            "scene": "S_NORMAL",
            "name": "MoonlightBH",
            "disable_regist": False,
            "enable_email_captcha": False,
            "thirdparty": ["tw"],
            "disable_mmt": False,
            "server_guest": False,
            "thirdparty_ignore": {},
            "enable_ps_bind_account": False,
            "thirdparty_login_configs": {
                "tw": {"token_type": "TK_GAME_TOKEN", "game_token_expires_in": 2592000},
            },
        },
    }


@app.route("/combo/box/api/config/sdk/combo")
def route_config_sdk_combo():
    return {
        "retcode": 0,
        "message": "OK",
        "data": {
            "vals": {
                "kibana_pc_config": {
                    "enable": 1,
                    "level": "Debug",
                    "modules": ["download"],
                    "list_price_tierv2_enable": False,
                    "network_report_config": {
                        "enable": 1,
                        "status_codes": [206],
                        "url_paths": ["dataUpload", "red_dot"]
                    }
                }
            }
        }
    }


@app.route("/bh3_usa/combo/granter/api/getConfig")
def route_combo_granter_api_getConfig():
    return {
        "retcode": 0,
        "message": "OK",
        "data": {
            "protocol": True,
            "qr_enabled": False,
            "log_level": "DEBUG",
            "announce_url": "http://localhost/announce",
            "push_alias_type": 2,
            "disable_ysdk_guard": False,
            "enable_announce_pic_popup": False,
        },
    }


@app.route('/admin/mi18n/plat_oversea/m2020030410/m2020030410-version.json')
def route_2020030410_m2020030410():
    return {"version": 67}


@app.route("/device-fp/api/getExtList")
def route_device_fp_api_getExtList():
    return {
        "retcode": 0,
        "message": "OK",
        "data": {
            "code": 200,
            "msg": "ok",
            "ext_list": [
                "cpuName",
                "systemName",
                "systemType",
                "deviceUID",
                "gpuID",
                "gpuName",
                "gpuAPI",
                "gpuVendor",
                "gpuVersion",
                "gpuMemory",
                "osVersion",
                "cpuCores",
                "cpuFrequency",
                "gpuVendorID",
                "isGpuMultiTread",
                "memorySize",
                "screenSize",
                "engineName",
                "addressMAC"
            ],
            "pkg_list": []
        }
    }

# Dispatch Handlers


@app.route("/query_dispatch")
def dispatch():
    return {
        "region_list": [
            {
                "dispatch_url": "http://localhost/query_gateway",
                "ext": {
                    "ai_use_asset_boundle": "1",
                    "block_error_dialog": "0",
                    "ex_res_use_http": "1",
                    "ex_resource_url_list": [
                        "d2wztyirwsuyyo.cloudfront.net/tmp/com.miHoYo.bh3global",
                        "bigfile-aliyun-usa.honkaiimpact3.com/tmp/com.miHoYo.bh3global"
                    ],
                    "is_xxxx": "0",
                    "mtp_switch": "0",
                    "network_feedback_enable": "1",
                    "res_use_asset_boundle": "0",
                    "show_bulletin_button": "0",
                    "show_bulletin_empty_dialog_bg": "0",
                    "show_version_text": "0",
                    "update_streaming_asb": "0",
                    "use_multy_cdn": "0"
                },
                "name": "MoonlightBH",
                "retcode": 0,
                "title": "MoonlightBH"
            }
        ],
        "retcode": 0
    }


@app.route("/query_gateway")
def gateway():
    return {
        "account_url": "http://localhost/account",
        "account_url_backup": "http://localhost/account",
        "asset_bundle_url_list": [
            "http://d2wztyirwsuyyo.cloudfront.net/asset_bundle/eur01/1.1",
            "http://bundle-aliyun-usa.honkaiimpact3.com/asset_bundle/eur01/1.1"
        ],
        "ex_audio_and_video_url_list": [],
        "ex_resource_url_list": [
            "d2wztyirwsuyyo.cloudfront.net/tmp/com.miHoYo.bh3global",
            "bigfile-aliyun-usa.honkaiimpact3.com/tmp/com.miHoYo.bh3global"
        ],
        "ext": {
            "ai_use_asset_boundle": "1",
            "block_error_dialog": "0",
            "ex_res_use_http": "1",
            "ex_resource_url_list": [
                "d2wztyirwsuyyo.cloudfront.net/tmp/com.miHoYo.bh3global",
                "bigfile-aliyun-usa.honkaiimpact3.com/tmp/com.miHoYo.bh3global"
            ],
            "is_xxxx": "0",
            "mtp_switch": "0",
            "network_feedback_enable": "1",
            "res_use_asset_boundle": "0",
            "show_bulletin_button": "0",
            "show_bulletin_empty_dialog_bg": "0",
            "show_version_text": "1",
            "update_streaming_asb": "0",
            "use_multy_cdn": "0"
        },
        "gameserver": {
            "ip": "127.0.0.1",
            "port": 7070
        },
        "gateway": {
            "ip": "127.0.0.1",
            "port": 7070
        },
        "is_data_ready": True,
        "msg": "",
        "oaserver_url": "http://localhost/oaserver",
        "region_name": "MoonlightBH",
        "retcode": 0,
        "server_cur_time": 1670072875,
        "server_cur_timezone": 1,
        "server_ext": {
            "cdkey_url": "http://localhost/cdkey",
            "mihoyo_sdk_env": "2"
        }
    }


# Index Handlers

@app.route('/combo/box/api/config/sw/precache')
def precache():
    return {"code": 0}


@app.route('/crash/dataUpload', method="POST")
def dataUpload():
    return {"code": 0}


@app.route('/data_abtest_api/config/experiment/list', method="POST")
def experiment_list():
    return {
        "retcode": 0,
        "success": True,
        "message": "",
        "data": [
            {
                "code": 1010,
                "type": 2,
                "config_id": "14",
                "period_id": "",
                "version": "",
                "configs": {
                    "cardType": "old"
                }
            }
        ]
    }


@app.route('/bh3_usa/mdk/agreement/api/getAgreementInfos')
def getAgreementInfos():
    return {
        "retcode": 0,
        "message": "OK",
        "data": {
            "marketing_agreements": []
        }
    }


@app.route('/report', method='POST')
def report():
    return {"code": 0}


def run_http_server(host):
    print('[HTTP] Listening on http://127.0.0.1:80/')
    app.run(host=host, port=80, quiet=True)
