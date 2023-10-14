import sys
import requests
import urllib.parse
from colorama import Fore, Style

endpoints = [
    "/graphql",
    "/api/graphql",
    "/graphql/v1",
    "/v1/graphql",
    "/v2/graphql",
    "/v3/graphql",
    "/v4/graphql",
    "/v5/graphql",
    "/graphql-api",
    "/api/v1/graphql",
    "/api/v2/graphql",
    "/graphql/v2",
    "/graphql/v3",
    "/graphql/v4",
    "/graphql/v5",
    "/v1/api/graphql",
    "/v2/api/graphql",
    "/v3/api/graphql",
    "/v4/api/graphql",
    "/v5/api/graphql",
    "/data/graphql",
    "/v1/data/graphql",
    "/v2/data/graphql",
    "/v3/data/graphql",
    "/v4/data/graphql",
    "/v5/data/graphql",
    "/api/data/graphql",
    "/api/v1/data/graphql",
    "/api/v2/data/graphql",
    "/api/v3/data/graphql",
    "/api/v4/data/graphql",
    "/api/v5/data/graphql",
    "/data/api/graphql",
    "/data/v1/graphql",
    "/data/v2/graphql",
    "/data/v3/graphql",
    "/data/v4/graphql",
    "/data/v5/graphql",
    "/v1/data/api/graphql",
    "/v2/data/api/graphql",
    "/v3/data/api/graphql",
    "/v4/data/api/graphql",
    "/v5/data/api/graphql",
    "/api/v1/data/api/graphql",
    "/api/v2/data/api/graphql",
    "/api/v3/data/api/graphql",
    "/api/v4/data/api/graphql",
    "/api/v5/data/api/graphql",
    "/data/v1/api/graphql",
    "/data/v2/api/graphql"
]

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
