from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from cycle_engine import CycleEngine

app = FastAPI()
engine = CycleEngine()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CycleInput(BaseModel):
    gt_temp: float
    comp_ratio: float
    htc_press: float
    biomass_flow: float

@app.post("/analyze")
async def analyze_cycle(data: CycleInput):
    results = engine.analyze_ad_htc_system(
        gt_temp_c=data.gt_temp,
        comp_ratio=data.comp_ratio,
        htc_press_bar=data.htc_press,
        biomass_flow_kgs=data.biomass_flow
    )
    return results

app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
