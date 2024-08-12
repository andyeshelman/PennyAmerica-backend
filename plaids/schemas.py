from ninja import Schema

class SandboxPublicTokenRequest(Schema):
    institution_id: str

class PublicTokenRequest(Schema):
    token: str