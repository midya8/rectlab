import test from'node:test';import assert from'node:assert/strict';import fs from'node:fs';import{solve,replay,validate}from'../docs/engine.mjs';
const data=JSON.parse(fs.readFileSync(new URL('./fixtures.json',import.meta.url)));
test('64 complete Python/browser reports agree',()=>{for(let i=0;i<data.inputs.length;i++)assert.deepEqual(solve(data.inputs[i]),data.reports[i]);for(const r of data.reports)assert.equal(replay(r),true)});
test('every small-control primitive noninput forgery rejected',()=>{for(const p of data.forgery_paths){const q=structuredClone(data.forgery_base);let v=q;for(const k of p.slice(0,-1))v=v[k];const k=p.at(-1),old=v[k];v[k]=typeof old==='boolean'?!old:typeof old==='number'?old+1:typeof old==='string'?old+'x':0;assert.throws(()=>replay(q))}});
test('strict finite boundary',()=>{for(const x of [{},{matrix:[]},{matrix:[[true]]},{matrix:[[2]]},{matrix:[[0],[1,0]]},{matrix:Array(3).fill(Array(5).fill(1))},{matrix:[[0]],extra:0}])assert.throws(()=>validate(x))});
