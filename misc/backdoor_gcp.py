import requests, json, sys

def main(public_key=None):
    access_token  = get_access_token()
    project_name  = get_project_name()
    instance_name = get_instance_name()
    zone          = get_instance_zone()
    print "Got Access Token: {}...".format(access_token[:20])
    print "Got project name: {}...".format(project_name)
    print "Got instance name: {}...".format(instance_name)
    print '='*80
    project_keys = get_project_keys(access_token)
    instance_keys = get_instance_keys(access_token)
    print len(project_keys), "keys for the project"
    print len(instance_keys), "keys for this instance"
    print '='*80

    if not public_key:
        print "No public key provided, exiting."
        sys.exit(0)

    project_keys.append(public_key)
    instance_keys.append(public_key)

    print "Adding key to this instance"
    print update_instance_keys(access_token, instance_keys, project_name, zone, instance_name)
    print "Adding key to the project"
    print update_project_keys(access_token, project_keys, project_name)


def make_authenticated_request(url, bearer_token, post_data=None):
    headers = {
        "Metadata-Flavor": "Google",
        "Authorization": "Bearer {}".format(bearer_token)
    }

    if post_data is not None:
        headers.update({"Content-Type": "application/json"})
        http_response = requests.post(url, headers=headers, data=json.dumps(post_data)).text
    else:
        http_response = requests.get(url, headers=headers).text

    if http_response and http_response[0] == "{":
        return json.loads(http_response)
    else:
        return http_response

def make_unauthenticated_request(url):
    headers = {
        "Metadata-Flavor": "Google"
    }

    http_response = requests.get(url, headers=headers).text
    if http_response[0] == "{":
        return json.loads(http_response)
    else:
        return http_response

def update_project_keys(access_token, keys, project_name):
    return make_authenticated_request(
        "https://www.googleapis.com/compute/v1/projects/{}/setCommonInstanceMetadata".format(project_name),
        access_token,
        {"items": [
            {"key": "ssh-keys", "value": "\n".join(keys)}
        ]})

def get_project_keys(access_token):
    return make_authenticated_request(
        "http://metadata.google.internal/computeMetadata/v1/project/attributes/ssh-keys",
        access_token
    ).split("\n")

def update_instance_keys(access_token, keys, project_name, zone, instance_name):
    fingerprint = make_authenticated_request(
    "https://www.googleapis.com/compute/v1/projects/{}/zones/{}/instances/{}".format(project_name, zone, instance_name),
    access_token
    )

    if 'metadata' not in fingerprint:
        raise Exception("Couldn't extract metadata fingerprint: "+fingerprint['error']['message'])

    fingerprint = fingerprint['metadata']['fingerprint']
    return make_authenticated_request(
        "https://www.googleapis.com/compute/v1/projects/{}/zones/{}/instances/{}/setMetadata".format(project_name, zone, instance_name),
        access_token,
        {"fingerprint": fingerprint, "items": [{"key": "ssh-keys", "value": "\n".join(keys)}]}
    )


def get_instance_keys(access_token):
    return make_authenticated_request(
        "http://metadata.google.internal/computeMetadata/v1/instance/attributes/ssh-keys",
        access_token
    ).split("\n")


def get_instance_zone():
    return make_unauthenticated_request(
        "http://metadata.google.internal/computeMetadata/v1/instance/zone",
    ).split("/")[-1]

def get_instance_name():
    return make_unauthenticated_request(
        "http://metadata.google.internal/computeMetadata/v1/instance/name",
    )

def get_access_token():
    return make_unauthenticated_request(
        "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"
    )['access_token']

def get_project_name():
    return make_unauthenticated_request(
        "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    )

if __name__ == "__main__":
    public_key = None
    if len(sys.argv) > 1:
        public_key = sys.argv[1]

    main(public_key)

