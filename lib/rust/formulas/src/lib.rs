#[macro_use] extern crate cpython;

use std::f64;
use cpython::{Python, PyResult};

fn hertz(force: f64, r: f64, delta_z: f64) -> f64 {
     (force*3.0) / (r.sqrt() * 4.0 * delta_z.powf(2.0))
}

fn hertz_py(_: Python, a: f64, b: f64, c: f64) -> PyResult<f64> {
    let out = hertz(a, b, c);
  	Ok(out) // To build a Python compatible module we need an intialiser which expose the public interface
}


fn sneddon(force: f64, mi_k: f64, alpha: f64, delta_z: f64) -> f64 {
    let a = force / delta_z.powf(2.0);
    f64::consts::PI * ( 1.0 - mi_k.powf(2.0)) * a / ( 2.0 * alpha.tan()) 
}

fn sneddon_py(_: Python, a: f64, b: f64, c: f64, d: f64) -> PyResult<f64> {
    let out = sneddon(a, b, c, d);
  	Ok(out) // To build a Python compatible module we need an intialiser which expose the public interface
}



py_module_initializer!(libformulas, initlibformulas, PyInit_libformulas, |py, m| {
    try!(m.add(py, "hertz", py_fn!(py, hertz_py(force: f64, r: f64, delta_z: f64))));
    try!(m.add(py, "sneddon", py_fn!(py, sneddon_py(force: f64, mi_k: f64, alpha: f64, delta_z: f64))));
    // Initialiser's macro needs a Result<> as return value
    Ok(())
});

