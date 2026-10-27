# Test plan before production
- Health endpoint responds successfully.
- Case create/read/update/delete works.
- Invalid lengths and malformed dates are rejected.
- Once authentication is added: user A cannot list/read/update/delete user B's cases.
- Deadline logic must test weekends, holidays, and jurisdiction-specific rules where applicable.
- Uploaded documents must be size-limited, malware-scanned, stored outside public paths, and deleted on request.
- AI-generated claims must cite a primary source and quote exact report evidence; unsupported claims must be flagged for review.
