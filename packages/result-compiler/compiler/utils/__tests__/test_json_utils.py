from compiler.utils.json_utils import read_from


def test_read():
    json = read_from("results/dav.json")
    print(json.splitlines()[:20])


# def test_write_to_known_dir():
#     data = "Hello World!"
#     write_to("student-data/foo.txt", data)

# def test_write_to_unknown():
#     data = "Hello World!"
#     write_to("unknown/foo.txt", data)
