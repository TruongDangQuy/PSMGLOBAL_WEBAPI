from sqlalchemy.orm import Session

from . import models

#valid_token
def valid_token_in(token : str, db: Session):
    return db.query(models.CredentialIn).filter(models.CredentialIn.Token == token , models.CredentialIn.IsUsed == '1').first()

#valid_xtoken
def valid_xtoken_in(xtoken : str, db: Session):
    return db.query(models.CredentialIn).filter(models.CredentialIn.XToken == xtoken , models.CredentialIn.IsUsed == '1').first()
