from google.auth import identity_pool
from google.auth.transport.requests import Request
from utils import CustomerSubjectTokenSupplier, audience


def test_identity_pool_credentials_refresh_succeeds():
    supplier = CustomerSubjectTokenSupplier()
    
    credentials = identity_pool.Credentials(
        audience=audience,
        subject_token_type="urn:ietf:params:oauth:token-type:jwt",
        subject_token_supplier=supplier,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )

    credentials.refresh(Request())

    assert credentials.token is not None
