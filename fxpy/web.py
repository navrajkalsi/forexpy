import requests
import pycountry
from bs4 import BeautifulSoup

# Uses API request
def remitly(sender_country, receiver_country, sender_currency, receiver_currency):
    
    # Returns JSON object with transaction rate 
    response = requests.get(f"https://api.remitly.io/v3/calculator/estimate?conduit={sender_country.alpha_3}%3A{sender_currency.alpha_3}-{receiver_country.alpha_3}%3A{receiver_currency.alpha_3}&anchor=SEND&amount=100&purpose=OTHER&customer_segment=ACTIVATED_SENDER&strict_promo=false")

    try:
        return float(response.json()['estimate']['exchange_rate']['base_rate'])
    except:
        return None

# Uses webpage scraping
def google(sender_currency, receiver_currency):
    
    response = requests.get(f"https://www.google.com/search?q={sender_currency.alpha_3}+to+{receiver_currency.alpha_3}")

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # Should be expected as '00.00 Receiver Currency' usually
        inr = soup.find('div', class_='BNeawe iBp4i AP7Wnd').text.split(' ')[0] # Splitting around blank space
        return float(inr.strip())
    except:
        return None

# Uses API request
def wise(sender_currency, receiver_currency):
    """ COMMENT USES WEBPAGE SCRAPPING (SLOW)
    response = requests.get("https://wise.com/gb/currency-converter/cad-to-inr-rate?amount=1")

    soup = BeautifulSoup(response.text, 'html.parser')

    #should be expected as the final inr amount
    inr = soup.find('span', class_='text-success').text

    return inr
    """

    # URL and Headers
    url = f"https://api.wise.com/v1/rates?source={sender_currency.alpha_3}&target={receiver_currency.alpha_3}"
    headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9,en-IN;q=0.8",
            "Content-Type": "application/json",
            "Authorization": "Basic OGNhN2FlMjUtOTNjNS00MmFlLThhYjQtMzlkZTFlOTQzZDEwOjliN2UzNmZkLWRjYjgtNDEwZS1hYzc3LTQ5NGRmYmEyZGJjZA==",
            "DNT": "1",
            "Origin": "https://wise.com",
            "Priority": "u=1,i",
            "Referer": "https://wise.com/",
            "Sec-Ch-Ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            }

    # Make the GET request
    # Response is a single elm list with a dictionary containing the rate variable
    response = requests.get(url, headers=headers)

    try:
        return round(response.json()[0]['rate'], 2)
    except:
        return None

# Uses API request
def cibc(sender_currency, receiver_currency):
    
    # CIBC only supports transfers originating from Canada
    if sender_currency.alpha_3 != 'CAD':
        return None

    # Returns JSON object with transaction rate of 1cad to inr
    response = requests.get(f"https://www.cibconline.cibc.com/ebm-pno/api/v1/json/public/fxCurrentRate?currency={receiver_currency.alpha_3}&productCode=GMT")

    try:
        return round(1/float(response.json()['rate']), 2)
    except:
        return None

# Uses API request
def westernUnion(sender_country, receiver_country, sender_currency, receiver_currency):

    # Western union uses post request to this url with headers and cookies attached and a JSON payload
    # Using post request
    url = "https://www.westernunion.com/router/"

    headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
            "content-type": "application/json",
            "device-id": "76139dc4-473b-4c74-ae05-1b969e90deac",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "wucountrycode": "CA",
            "wulanguagecode": "en",
            "x-wu-accesscode": "RtYV3XDz9EA",
            "x-wu-operationname": "products",
            "cookie": "AKCountry=CA; AKRegioncode=ON; AKAreacode=; AKCounty=; WULanguageCookie_=en; s_ecid=MCMID%7C75725541329991950550142014113139011936; ... (truncated for brevity)",
            "Referer": "https://www.westernunion.com/ca/en/currency-converter/cad-to-inr-rate.html",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }

    body = {
            "query": """
            query products($req_products: ProductsInput, ) {
                products(input: $req_products) {
                    __typename
                    ...on ProductsResponse {
                        products {
                            code
                            name
                            payIn
                            payOut
                            fees
                            exchangeRate
                            destination {
                                expectedPayoutAmount
                                expectedPayoutAmountLong
                                currencyIsoCode
                                countryIsoCode
                                splitPayOut {
                                    expectedPayoutAmount
                                    currencyIsoCode
                                    exchangeRate
                                    countryIsoCode
                                    }
                                actualPayoutAmount
                                }
                            }
                        categories {
                            type
                            orders {
                                payIn
                                payOut
                                }
                            }
                        }
                    ...on ErrorResponse {
                        errorCode
                        message
                        }
                    }
                }
            """,
            "variables": {
                "req_products": {
                    "origination": {
                        "channel": "WWEB",
                        "client": "WUCOM",
                        "countryIsoCode": f"{sender_country.alpha_2}",
                        "currencyIsoCode": f"{sender_currency.alpha_3}",
                        "eflType": "STATE",
                        "amount": 1,
                        "fundsIn": "*",
                        "airRequested": "Y",
                        "eflValue": "ON"
                        },
                    "destination": {
                        "countryIsoCode": f"{receiver_country.alpha_2}",
                        "currencyIsoCode": f"{receiver_currency.alpha_3}"
                        },
                    "language": "en",
                    "headerRequest": {
                        "version": "0.5",
                        "requestType": "PRICECATALOG",
                        "correlationId": "web-83c5c07a-d8e3-464c-a768-feb0bde2bad2",
                        "transactionId": "web-83c5c07a-d8e3-464c-a768-feb0bde2bad2-1734750234145"
                        },
                    "visit": {
                        "localDatetime": {
                            "timeZone": 300,
                            "timestampMs": 1734750234145
                            }
                        }
                    }
                }
        }

    # WU uses post rather than get request
    response = requests.post(url, headers=headers, json=body)

    try:
        return round(response.json()['data']['products']['products'][0]['exchangeRate'], 2)
    except:
        return None

# Uses API request
def xe(sender_country, receiver_country, sender_currency, receiver_currency):

    url = "https://launchpad-api.xe.com/v2/quotes"

    headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
            "content-type": "application/json",
            "device-id": "e047dbd5-9016-4152-8557-a519929a920d",
            "dnt": "1",
            "origin": "https://www.xe.com",
            "priority": "u=1, i",
            "referer": "https://www.xe.com/",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            "x-correlation-id": "XECOM-be309ab7-6134-4c96-aa64-e7760f14fbe8"
        }

    body = {
            "sellCcy": f"{sender_currency.alpha_3}",
            "buyCcy": f"{receiver_currency.alpha_3}",
            "userCountry": f"{sender_country.alpha_2}",
            "amount": 1,
            "fixedCcy": f"{sender_currency.alpha_3}",
            "countryTo": f"{receiver_country.alpha_2}"
        }

    response = requests.post(url, headers=headers, json=body)

    try:
        return response.json()['quote']['individualQuotes'][0]['rate']
    except:
        return None

# Uses API request
def moneygram(sender_country, receiver_country, sender_currency):

    url = f"https://consumerapi.moneygram.com/services/capi/api/v1/sendMoney/fx?senderCountryCode={sender_country.alpha_3}&receiverCountryCode={receiver_country.alpha_3}&senderCurrencyCode={sender_currency.alpha_3}&captchaResponse=03AFcWeA7WD2Oj9yz802qEL6iZzi6b-WgmTKdywzpR2cogHGblEYzqwFvv28w-iFfZTgUjAnxZuy85osm05tZSwbRLGrvffVZeFyIH8Q-Z7nOrqGqDDjd-0TOEB6ujq3t4O292yJgaLJN2CZk0IbtOBDl9MtMLw_PUbPzMNW8sUqpCZJv5SQ2DBoP70XcEmzoPRPH7TQt0qWw5ZjfrCVScggpmcaKDYgsSMpTJZRiMRtZCwZrnHBX7QT8zGYeKR0z4MF0TkHSAJgQs3whdeuBnmaVqpr-8z3r0a6MaKiOIcpJgVYXTZqISNlTq8Oy8BKDEyNh_87oMFEknIXkEs3qUgA9kjW2jUgS4OK5igtjQPG255Z2Lk64soZvVPSNK4LF4fmyKWlyUeuzzwuWi4XJFDcf5SvHo2OmxpOlFr84vfBuRjan8S25RGawT2elK7Wf9cy729VYxsF-Gkd3Ibd5BTiXg4XhjKLHv-d8eSODNFay8xwGjW7g_aZXyrej-z5VeFz-4uaqbne-PHlLalbg7MPLzWAwIXW4YPou9cco0kwd-YbQFikwOmw4l_58pR2Ataxm10t4__A_QwPaoUma_gksuMqGkPpPauYSaD0p0DWLsjHCa-YsW3GPg3R0v_82VbTmJnCOxVp-09PThdnTo1UflTx8aDFTFELQ459cDxthFyx9v0Vgan0iBTzkS8TkrCOkHXeWLvueb5EW2KDveQ9oxfqbmkGGrletE2EWEqhLFKILyuiWvTS0XGh-itt13Ya9Gh0JWUAnzcaFGjf-vImNVBiZ_RZ5KNRaS2YL0O9KE0FGvWlEknHzchaQuCA89bjpgPm7yzyDViOCDKS0dEvnOpMH8HK6fmJXcvnRLjvUCzh4Rysi0JFv_hcwo0yB-zGq0oSlwkJVqgbsVhNJm1voWcrN5VKayreytUzYKkwjAAvaS6ai0sBFcNpCwjAeC7MCwVQ6KoJiyujA9R_W1IatvapJ18Sr3Oh4Y4SAdw0zT7S9rAsq_X4Qtg0Fg21qYMsfM6Thex3BoFcuXwcRuj_HDPGkLWd2nkH86z5aZJiPcRJzecywro6ND5j_kf-Q6B65wqjl6BnpXuRH1oKWIs3DYedGFncWPI_gGD5ksvq8TC7FdACuer3BHNqm1CsmOY6MhYbxwuLMEGCP2hqkUo5aOiTj4rEB4Wv8ojdshY_U_U0Yhwm-GnwWs03V3ar9dJ6UveiLkQszAR_yy4jvh5-3BsMlfe2ptoOsQGBqXbdDGNsd2TE6qBK4Hg5HwBvcagHOhQnM9eQml7M_rzkIydXL7cPCuw71tB7Kw3PLr3xfkcFruP-sTM3OaHNt_OG0h73y1ctz0pgj4-TWzO5wxjhEK_1Un0bsPNaWzPlVV_PJPD1youjx7uMYXQItm-2zH0m7MaiQIdxmsZnpW47Rzb-LgB3QSDUcwqz13y3yNxacG-iHvFkVVJtRKMp8rgC6fJDVHtyLlZBZtZRsErAWP-5u_YDeAxUwY2q_PMXYZmSFsYn6DIJ5x-fLOKqzKuboZ_N4nHgiNyV_6o6f_FJO7vnbDI7rh88BJnxLd5weZ4lxQSEUxJff2nB2FyC0TFhN2iX8bhrsxowf1hIMD6OxR7nVhMKXpUlNKUFzeuHXE2nliXq1QgmoSdFA1szc1QzdTU_ORZIX9W1BggVAm8ivP2P-fQU5F6necck3r_GTUsI_Pcz0a63W7QEAQyfp4G1V8eM01JE_pkfc_Eq5NBV81Ioy-fjF_wKsnDelwPdU-EAQClWAVAc3ESFgs1z7b92lzlFmUFEHTV6kVP96-gsRo2riiMzBTB4OQ3hqKcACbFG1yaBCfcUwloiqdnaakS-jyKuWCCH60viUxqRvt4I4n5oXkHwMvP35IxW5c_8CfJ5Aj1vytxnJlNWY"

    headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
            "clientkey": "Basic V0VCX2VkYjI0ZDc5LTA0ODItNDdlMi1hNmQ2LTc4ZGY5YzI4MmM0ZTo1MTNlMTEyOS0yZTJmLTRlYmUtYjkwMi02YTVkMGViMDNjZjc=",
            "cookie": "visid_incap_2222183=s7aSdrONSEOC+slHM4poJDEhX2cAAAAAQUIPAAAAAADzWy9us3Ndlbn2uoU+8L8N; nlbi_2222183=I/EpESsnMjgwKqQKUnWprgAAAAAGmUDI/dqLLuLF+PnwrPEJ; _gcl_au=1.1.2076344448.1734287667; notice_behavior=implied,us; _cs_c=0; _cs_cvars=%7B%221%22%3A%5B%22country_code%22%2C%22undefined%22%5D%2C%222%22%3A%5B%22lang_code%22%2C%22en%22%5D%2C%223%22%3A%5B%22receiving_country%22%2C%22undefined%22%5D%2C%225%22%3A%5B%22client_type%22%2C%22unknown%22%5D%7D; visid_incap_2163526=IdMWHcN+QPCeocAyKZrPxzQhX2cAAAAAQUIPAAAAAABxf35O+OEOg5l21c22ROuL; IR_gbd=moneygram.com; nlbi_2163526=wLVLNn1+YXx/Vu26B1D/egAAAADpywU9DsEdCJYi/Lfob4rl; afUserId=a4feb3aa-fe14-4582-80c0-6daca6f76536-p; AF_SYNC=1734287669614; _tt_enable_cookie=1; _ttp=yJynDOt-No78KEXr8nJ6UMyka1s.tt.1; _ga=GA1.1.854567183.1734287671; usi_return_visitor=Sun%20Dec%2015%202024%2013%3A34%3A31%20GMT-0500%20(Eastern%20Standard%20Time); notice_preferences=3:; notice_gdpr_prefs=0,1,2,3:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3,4; incap_ses_1369_2222183=AjKUDvmzJm2+tlW5dKr/EoQiYGcAAAAAfwIPSUxyic9JDj/wIHgPGw==; incap_ses_1446_2222183=wWC5DjFVhX0HnpOgjjkRFNL7YWcAAAAA+rSHe5xRunz/ge0kgfy9UA==; incap_ses_1848_2222183=lEQ2WMkYp0eRMtiWUWqlGT7zZmcAAAAATo4pXu/LNFIsfkN7Jtw0WA==; TAsessionID=b8abf682-acd9-4b8f-b96d-672cdf6e95d5|EXISTING; incap_ses_1848_2163526=lK3tNmk4mgMZPdiWUWqlGUHzZmcAAAAAKDvyEPYcWwJkVat//1SLug==; reese84=3:FyIa2S2eyyOFdmsCgPl58w==:GJcQARkQWAtsctqKRWGK4rc7UyE98iSRq4Bq4zLUS7N/r49adbccvtcYSE4scDdE25bh9KIdfEHAW7aWgADnh5CExkyCh+STkFgLDsDrb0pFk1wNveEm7+Qi8UU7H7Jg4/l1dxSJ5RHBDgsD93lhIrTwCwU3gd1sjlArd0OczeoJm57hAZanfvO0WwQQWxpYaQZzimyZKenDtWS87+pyN4Z9vozNqpQUl7MUpHr1QTiX8J2Fco+OrY+L1fmwSyFQtZ32LEGPDuwLdf6zWgLdGvOjmH5is6hzO0qWggugESlwggMh0cC2pfrvEaIsGVMJUd9oMRxA1j0RjW53GQaUOpoyqHNDygR2+8etcHMIVkvnYnoN04Q///OGobLIQa3+F6z+PfMnnySgpYqmLlha1w+eBH/NZhcNXTu8P3fYY9eJxpTj3YRrVgQRvFITK604E6Z3+siKiLq7wyL9feAUgA==:h2247gdePt5kBJi5wpuvIMXxuaHBphnwyIf395eCvcA=; _clck=15ir57e%7C2%7Cfrw%7C0%7C1810; nlbi_2222183_2147483392=a4euXiaW/EtEHPw9UnWprgAAAADJgJP6SjxKU6y9Tk9TQBoF; _cs_id=99272d44-fa3d-a8e4-fbf9-28d829dfeda9.1734287667.16.1734800206.1734800190.1.1768451667827.1; _uetsid=88bd8140bfbc11efb898ad631a97a889; _uetvid=3956b620bb1311efad6debf2faf2660a; IR_16828=1734800206547%7C0%7C1734800206547%7C%7C; _cs_s=2.5.0.9.1734802006576; _ga_419TZ53GJ4=GS1.1.1734800192.8.1.1734800207.0.0.0; _clsk=t8mt0j%7C1734800207473%7C2%7C1%7Cu.clarity.ms%2Fcollect",
            "dnt": "1",
            "locale-header": "en_CA",
            "origin": "https://www.moneygram.com",
            "priority": "u=1, i",
            "referer": "https://www.moneygram.com/",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            "x-correlation-id": "XECOM-be309ab7-6134-4c96-aa64-e7760f14fbe8"
        }

    response = requests.get(url, headers=headers)

    try:
        return round(response.json()['exchangeRate'], 2)
    except:
        return None

# Verifies the return values of all the conversions
def verify_conversion(service_name, conversion, sender_currency, receiver_currency):
    
    if conversion is None:
        print(f"{service_name} does not support currency conversion from {sender_currency.alpha_3} to {receiver_currency.alpha_3}.")
        return service_name, "No support"
    else:
        print(f"{service_name}: {conversion}")
        return service_name, conversion

# Function to call all the service functions
def do_conversion(countries):
    sender_country = countries[0]
    receiver_country = countries[1]

    # Retrieving currency codes here rather than doing so for every site function
    sender_currency = pycountry.currencies.get(numeric = sender_country.numeric)
    receiver_currency = pycountry.currencies.get(numeric = receiver_country.numeric)

    print(f"\nHere are all the currency conversion rates from {sender_currency.alpha_3} to {receiver_currency.alpha_3}:\nEvery conversion is from 1 {sender_currency.alpha_3} to __.__ {receiver_currency.alpha_3}.\n")

    # List to return with all the conversions, used for final excel export
    conversions = []
    # Passing country objects because different sites require different country info, but all require currency codes
    conversions.append(verify_conversion('Google', google(sender_currency, receiver_currency), sender_currency, receiver_currency))
    conversions.append(verify_conversion('Western Union', westernUnion(sender_country, receiver_country, sender_currency, receiver_currency), sender_currency, receiver_currency))
    conversions.append(verify_conversion('MoneyGram', moneygram(sender_country, receiver_country, sender_currency), sender_currency, receiver_currency))
    conversions.append(verify_conversion('Wise', wise(sender_currency, receiver_currency), sender_currency, receiver_currency))
    conversions.append(verify_conversion('Remitly', remitly(sender_country, receiver_country, sender_currency, receiver_currency), sender_currency, receiver_currency))
    conversions.append(verify_conversion('CIBC', cibc(sender_currency, receiver_currency), sender_currency, receiver_currency))
    conversions.append(verify_conversion('Xe', xe(sender_country, receiver_country, sender_currency, receiver_currency), sender_currency, receiver_currency))
    
    return conversions

if __name__ == "__main__":

    # I personally mostly have to send money to India, therefore when I run this file I want to straight away get results for that.
    can_ind = (pycountry.countries.get(alpha_3 = 'CAN'), pycountry.countries.get(alpha_3 = 'IND'))
    
    do_conversion(can_ind)
