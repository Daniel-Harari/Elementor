from datetime import datetime
from db import db
import requests


class VirusTotalModel(db.Model):
    __tablename__ = 'virus_total_stats'
    domain = db.Column(db.String, primary_key=True)
    last_checked = db.Column(db.DateTime)
    harmless_count = db.Column(db.Integer)
    malicious_count = db.Column(db.Integer)
    suspicious_count = db.Column(db.Integer)
    undetected_count = db.Column(db.Integer)
    timeout_count = db.Column(db.Integer)
    vote_count = db.Column(db.Integer)

    def __init__(self, api_token, domain):
        self.token = {'x-apikey': api_token}
        self.domain = domain
        analysis_id = self.post_analyses(domain, self.token)
        r = self.get_analyses(analysis_id, self.token)
        self.harmless_count = r['stats'].get("harmless")
        self.malicious_count = r['stats'].get("malicious")
        self.suspicious_count = r['stats'].get("suspicious")
        self.undetected_count = r['stats'].get("undetected")
        self.timeout_count = r['stats'].get("timeout")
        self.vote_count = self.get_votes(domain, self.token)
        self.last_checked = datetime.now()

    @classmethod
    def find_by_domain(cls, domain):
        return cls.query.filter_by(domain=domain).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {"url": self.domain, "last_check_date": self.last_checked, "stats": {
            "harmless": self.harmless_count,
            "malicious": self.malicious_count,
            "suspicious": self.suspicious_count,
            "undetected": self.undetected_count,
            "timeout": self.timeout_count
        }, "vote_count": self.vote_count}

    @staticmethod
    def post_analyses(url, headers):
        payload = {"url": url}
        r = requests.post("https://www.virustotal.com/api/v3/urls", data=payload, headers=headers)
        analysis_id = r.json()['data'].get('id')
        return analysis_id

    @staticmethod
    def get_votes(url, headers):
        r = requests.get(f"https://www.virustotal.com/api/v3/domains/{url}/votes", headers=headers)
        return r.json()['meta'].get("count")

    @staticmethod
    def get_analyses(analyses_id, headers):
        r = requests.get(f"https://www.virustotal.com/api/v3/analyses/{analyses_id}", headers=headers)
        return r.json()['data'].get('attributes')

