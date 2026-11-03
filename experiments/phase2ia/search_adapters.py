"""Frozen R1/R3 demonstration-only search adapters for the WP6 runner.

Both callbacks use the registered flat candidate languages and stop at the
first exact fit or the shared maximum of ten evaluated candidates. No test-set
field is requested or accepted.
"""
from __future__ import annotations
import hashlib, json
from typing import Any, Mapping, Sequence

from experiments.phase13g.common import PROGRAMS, infer_context
from representations.r3 import Demonstration, ParseStatus, SearchStatus, parse_grid, run_search
from experiments.phase2ia.runner import SearchObservation


def _hash_candidate(prefix:str,payload:str)->str:
    return prefix+hashlib.sha256(payload.encode("utf-8")).hexdigest()


def search_r1(arm:str,task_id:str,demos:tuple[Mapping[str,Any],...],max_trials:int)->SearchObservation:
    if arm!="R1" or type(max_trials) is not int or not 1<=max_trials<=10:
        return SearchObservation("INVALID_INPUT","INVALID_INPUT",0,"INVALID_INPUT")
    if not demos: return SearchObservation("INVALID_INPUT","INVALID_INPUT",0,"INVALID_INPUT")
    for pair in demos:
        for field in ("input","output"):
            grid=parse_grid(pair[field])
            if grid.status is ParseStatus.INVALID_INPUT:
                return SearchObservation("INVALID_INPUT","INVALID_INPUT",0,"INVALID_INPUT")
    trial_ids=[]
    train=[{"input":p["input"],"output":p["output"]} for p in demos]
    for program in PROGRAMS[:max_trials]:
        context=infer_context(program,train)
        payload=json.dumps({"program":program,"context":context},sort_keys=True,separators=(",",":"),default=str)
        cid=_hash_candidate("R1-",payload)
        trial_ids.append(cid)
        if context is not None:
            return SearchObservation("PARSED","FOUND_EXACT_DEMO_FIT",len(trial_ids),
              "EXACT_FIT_FOUND",cid,program,tuple(trial_ids))
    reason="CANDIDATE_BUDGET_EXHAUSTED" if len(trial_ids)==max_trials else "NO_FIT_WITHIN_LANGUAGE"
    return SearchObservation("PARSED","NOT_FOUND_WITHIN_LANGUAGE_AND_BUDGET",len(trial_ids),
      reason,None,None,tuple(trial_ids))


def search_r3(arm:str,task_id:str,demos:tuple[Mapping[str,Any],...],max_trials:int)->SearchObservation:
    if arm!="R3" or type(max_trials) is not int or not 1<=max_trials<=10:
        return SearchObservation("INVALID_INPUT","INVALID_INPUT",0,"INVALID_INPUT")
    if not demos: return SearchObservation("INVALID_INPUT","INVALID_INPUT",0,"INVALID_INPUT")
    r3_demos=tuple(Demonstration(p["input"],p["output"]) for p in demos)
    parsed=[parse_grid(p["input"]) for p in demos]
    if any(p.status is ParseStatus.INVALID_INPUT for p in parsed):
        return SearchObservation("INVALID_INPUT","INVALID_INPUT",0,"INVALID_INPUT")
    search=run_search(r3_demos,max_trials=max_trials)
    trial_ids=tuple(t.candidate_id for t in search.trials)
    if search.status is SearchStatus.FOUND_EXACT_DEMO_FIT and search.candidate is not None:
        cid=search.candidate.candidate_id
        return SearchObservation("PARSED","FOUND_EXACT_DEMO_FIT",len(trial_ids),
          "EXACT_FIT_FOUND",cid,search.candidate.action,trial_ids)
    if search.status is SearchStatus.INVALID_INPUT:
        return SearchObservation("INVALID_INPUT","INVALID_INPUT",len(trial_ids),"INVALID_INPUT",None,None,trial_ids)
    reason="CANDIDATE_BUDGET_EXHAUSTED" if len(trial_ids)>=max_trials else "NO_FIT_WITHIN_LANGUAGE"
    return SearchObservation("PARSED","NOT_FOUND_WITHIN_LANGUAGE_AND_BUDGET",len(trial_ids),
      reason,None,None,trial_ids)


def registered_searchers()->dict[str,Any]:
    return {"R1":search_r1,"R3":search_r3}
