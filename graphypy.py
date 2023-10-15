import sys
import requests
import urllib.parse
from colorama import Fore, Style
from endpoints_worlist import endpoints


introspection_query = '''
    {__schema{queryType{name}mutationType{name}subscriptionType{name}types{...FullType}directives{name description locations args{...InputValue}}}}fragment FullType on __Type{kind name description fields(includeDeprecated:true){name description args{...InputValue}type{...TypeRef}isDeprecated deprecationReason}inputFields{...InputValue}interfaces{...TypeRef}enumValues(includeDeprecated:true){name description isDeprecated deprecationReason}possibleTypes{...TypeRef}}fragment InputValue on __InputValue{name description type{...TypeRef}defaultValue}fragment TypeRef on __Type{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name}}}}}}}}'''

def check_graphql_endpoints(base_url, endpoints):
    graphql_endpoints = []
    for endpoint in endpoints:
        url = base_url + endpoint
        print(f"Checking {url}...")
        try:
            response = requests.post(url, json={'query': introspection_query})
            if response.status_code == 200:
                graphql_endpoints.append(url)
                print(f"{Fore.GREEN}Detected GraphQL endpoint at {url}. Introspection query result:")
                print(response.json())
                break
            else:
                # Try GET request with query as a parameter
                get_url = f"{url}?query={introspection_query}"
                response = requests.get(get_url)
                if response.status_code == 200:
                    graphql_endpoints.append(url)
                    print(f"{Fore.GREEN}Detected GraphQL endpoint at {url}. Introspection query result:")
                    print(response.json())
                else:
                    # Try URL encoding of the introspection query
                    encoded_query = urllib.parse.quote(introspection_query)
                    encoded_url = f"{url}?query={encoded_query}"
                    response = requests.get(encoded_url)
                    if response.status_code == 200:
                        graphql_endpoints.append(url)
                        print(f"{Fore.GREEN}Detected GraphQL endpoint at {url}. Introspection query result:")
                        print(response.json())
        except requests.RequestException as e:
            print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
    return graphql_endpoints

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the base URL as a command-line argument.")
        sys.exit(1)

    base_url = sys.argv[1]
    detected_endpoints = check_graphql_endpoints(base_url, endpoints)
    if not detected_endpoints:
        print("No GraphQL endpoints detected.")
