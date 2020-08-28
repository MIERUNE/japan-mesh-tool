use std::env;
use std::fs::File;
use std::io::{BufWriter, Write};

const ORIGIN_MIN_LON: f64 = 122.0;
const ORIGIN_MAX_LON: f64 = 154.0;
const ORIGIN_MIN_LAT: f64 = 20.0;
const ORIGIN_MAX_LAT: f64 = 46.0;

struct Mesh {
    vertexes: Vec<Vec<f64>>,
    code: String,
}

struct Extent {
    leftbottom: (f64, f64),
    righttop: (f64, f64),
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let meshnum: u8 = args[1].parse().unwrap();

    let mut extent = Extent {
        leftbottom: (0.0, 0.0),
        righttop: (0.0, 0.0),
    };
    if args.len() > 2 {
        let lb_lonlat: Vec<&str> = args[2].split(",").collect();
        let rt_lonlat: Vec<&str> = args[3].split(",").collect();
        extent.leftbottom = (lb_lonlat[0].parse().unwrap(), lb_lonlat[1].parse().unwrap());
        extent.righttop = (rt_lonlat[0].parse().unwrap(), rt_lonlat[1].parse().unwrap());
    }
    let dist = format!("mesh_{}.geojsonl", meshnum);
    get_meshes(meshnum, extent, dist);
}

fn get_meshes(meshnum: u8, extent: Extent, dist: String) {
    let xy_size = get_mesh_size(meshnum);
    let x_mesh_count = ((ORIGIN_MAX_LON - ORIGIN_MIN_LON) / xy_size.0) as usize;
    let y_mesh_count = ((ORIGIN_MAX_LAT - ORIGIN_MIN_LAT) / xy_size.1) as usize;
    let mut xy_start_offset = (0, 0);
    let mut xy_end_offset = (0, 0);

    if extent.leftbottom != (0.0, 0.0) || extent.righttop != (0.0, 0.0) {
        xy_start_offset = get_start_offset(meshnum, extent.leftbottom);
        xy_end_offset = get_end_offset(meshnum, extent.righttop);
    }

    let file = File::create(dist).unwrap();
    let mut writer = BufWriter::new(file);
    for y in xy_start_offset.1..(y_mesh_count - xy_end_offset.1) {
        for x in xy_start_offset.0..(x_mesh_count - xy_end_offset.0) {
            let mesh_vertex = get_vertexes(meshnum, x, y);
            let mesh_code = get_meshcode(meshnum, x, y);
            let mesh = Mesh {
                vertexes: mesh_vertex,
                code: mesh_code,
            };
            let geojson_str = make_string(&mesh);
            writer.write(geojson_str.as_bytes()).unwrap();
        }
    }
}

fn make_string(mesh: &Mesh) -> String {
    let gj1 = String::from(r#"{"type":"Feature","properties":{"code":""#);
    let code = mesh.code.to_string();
    let gj2 = String::from(r#""},"geometry":{"type":"Polygon","coordinates":["#);
    let vertexes = format!("{:?}", mesh.vertexes);
    let gj3 = String::from(r#"]}}"#);
    format!("{}{}{}{}{}\n", gj1, code, gj2, vertexes, gj3)
}

fn get_meshcode(meshnum: u8, x: usize, y: usize) -> String {
    let mut meshcode = String::new();
    let xy_size = get_mesh_size(meshnum);
    let left_lon = ORIGIN_MIN_LON + xy_size.0 * x as f64;
    let bottom_lat = ORIGIN_MIN_LAT + xy_size.1 * y as f64;
    meshcode.push_str(&((bottom_lat * 1.5) as usize).to_string());
    meshcode.push_str(&(left_lon as usize).to_string()[1..]);
    match meshnum {
        1 => (),
        2 => {
            meshcode.push_str(&(y % 8).to_string());
            meshcode.push_str(&(x % 8).to_string());
        }
        3 => {
            meshcode.push_str(&(y % 80 / 10).to_string());
            meshcode.push_str(&(x % 80 / 10).to_string());
            meshcode.push_str(&(y % 10).to_string());
            meshcode.push_str(&(x % 10).to_string());
        }
        4 => {
            meshcode.push_str(&(y % 160 / 20).to_string());
            meshcode.push_str(&(x % 160 / 20).to_string());
            meshcode.push_str(&(y % 20 / 2).to_string());
            meshcode.push_str(&(x % 20 / 2).to_string());
            meshcode.push_str(&(y % 2 * 2 + x % 2 + 1).to_string());
        }
        5 => {
            meshcode.push_str(&(y % 320 / 40).to_string());
            meshcode.push_str(&(x % 320 / 40).to_string());
            meshcode.push_str(&(y % 40 / 4).to_string());
            meshcode.push_str(&(x % 40 / 4).to_string());
            meshcode.push_str(&(y % 4 / 2 * 2 + x % 4 / 2 + 1).to_string());
            meshcode.push_str(&(y % 2 * 2 + x % 2 + 1).to_string());
        }
        6 => {
            meshcode.push_str(&(y % 640 / 80).to_string());
            meshcode.push_str(&(x % 640 / 80).to_string());
            meshcode.push_str(&(y % 80 / 8).to_string());
            meshcode.push_str(&(x % 80 / 8).to_string());
            meshcode.push_str(&(y % 8 / 4 * 2 + x % 8 / 4 + 1).to_string());
            meshcode.push_str(&(y % 4 / 2 * 2 + x % 4 / 2 + 1).to_string());
            meshcode.push_str(&(y % 2 * 2 + x % 2 + 1).to_string());
        }
        7 => {
            meshcode.push_str(&(y % 800 / 100).to_string());
            meshcode.push_str(&(x % 800 / 100).to_string());
            meshcode.push_str(&(y % 100 / 10).to_string());
            meshcode.push_str(&(x % 100 / 10).to_string());
            meshcode.push_str(&(y % 10).to_string());
            meshcode.push_str(&(x % 10).to_string());
        }
        8 => {
            meshcode.push_str(&(y % 1600 / 200).to_string());
            meshcode.push_str(&(x % 1600 / 200).to_string());
            meshcode.push_str(&(y % 200 / 20).to_string());
            meshcode.push_str(&(x % 200 / 20).to_string());
            meshcode.push_str(&(y % 20 / 2).to_string());
            meshcode.push_str(&(x % 20 / 2).to_string());
            meshcode.push_str(&(y % 2).to_string());
            meshcode.push_str(&(x % 2).to_string());
        }
        9 => {
            meshcode.push_str(&(y % 1600 / 200).to_string());
            meshcode.push_str(&(x % 1600 / 200).to_string());
            meshcode.push_str(&(y % 200 / 20).to_string());
            meshcode.push_str(&(x % 200 / 20).to_string());
            meshcode.push_str(&(y % 20 / 2).to_string());
            meshcode.push_str(&(x % 20 / 2).to_string());
            meshcode.push_str(&(y % 10).to_string());
            meshcode.push_str(&(x % 10).to_string());
        }
        _ => (),
    }
    meshcode
}

fn get_vertexes(meshnum: u8, x: usize, y: usize) -> Vec<Vec<f64>> {
    let xy_size = get_mesh_size(meshnum);
    let left_lon = ORIGIN_MIN_LON + xy_size.0 * x as f64;
    let bottom_lat = ORIGIN_MIN_LAT + xy_size.1 * y as f64;
    let right_lon = ORIGIN_MIN_LON + xy_size.0 * (x + 1) as f64;
    let top_lat = ORIGIN_MIN_LAT + xy_size.1 * (y + 1) as f64;

    let geometry = vec![
        vec![left_lon, bottom_lat],
        vec![left_lon, top_lat],
        vec![right_lon, top_lat],
        vec![right_lon, bottom_lat],
        vec![left_lon, bottom_lat],
    ];
    geometry
}

fn get_start_offset(meshnum: u8, leftbottom: (f64, f64)) -> (usize, usize) {
    let xy_size = get_mesh_size(meshnum);
    let mut x_offset = 0;
    let mut y_offset = 0;
    while leftbottom.0 >= ORIGIN_MIN_LON + xy_size.0 * ((x_offset + 1) as f64) {
        x_offset += 1;
    }
    while leftbottom.1 >= ORIGIN_MIN_LAT + xy_size.1 * ((y_offset + 1) as f64) {
        y_offset += 1;
    }
    (x_offset, y_offset)
}

fn get_end_offset(meshnum: u8, righttop: (f64, f64)) -> (usize, usize) {
    let xy_size = get_mesh_size(meshnum);
    let mut x_offset = 0;
    let mut y_offset = 0;
    while righttop.0 <= ORIGIN_MAX_LON - xy_size.0 * ((x_offset + 1) as f64) {
        x_offset += 1;
    }
    while righttop.1 <= ORIGIN_MAX_LAT - xy_size.1 * ((y_offset + 1) as f64) {
        y_offset += 1;
    }
    (x_offset, y_offset)
}

fn get_mesh_size(meshnum: u8) -> (f64, f64) {
    match meshnum {
        1 => (1.0, 2.0 / 3.0),
        2 => (1.0 / 8.0, 1.0 / 12.0),
        3 => (1.0 / 80.0, 1.0 / 120.0),
        4 => (1.0 / 160.0, 1.0 / 240.0),
        5 => (1.0 / 320.0, 1.0 / 480.0),
        6 => (1.0 / 640.0, 1.0 / 960.0),
        7 => (1.0 / 800.0, 1.0 / 1200.0),
        8 => (1.0 / 1600.0, 1.0 / 2400.0),
        9 => (1.0 / 8000.0, 1.0 / 12000.0),
        _ => (0.0, 0.0),
    }
}
