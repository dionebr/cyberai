from fastapi import APIRouter

router = APIRouter()

TECHNIQUES = [
	"sql_injection",
	"xss",
	"rce",
	"lfi_rfi",
	"deserialization",
	"buffer_overflow",
	"privesc",
	"pivoting",
	"antivirus_evasion",
	"memory_analysis"
]

@router.get("/techniques")
async def get_techniques():
	return {"techniques": TECHNIQUES}
