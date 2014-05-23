#!/usr/bin/env bash

files=("/home/vinicius/Downloads/perf/65825-chrono-trigger-snes-screenshot-map-1000-ad-presents.png"
    "/home/vinicius/Downloads/perf/Castlevania_-_Aria_of_Sorrow_2012_12_23_22_24_42_958.png"
    "/home/vinicius/Downloads/perf/girl1_1.png"
    "/home/vinicius/Downloads/perf/jabier.png"
    "/home/vinicius/Downloads/perf/Secret of Mana.png"
    "/home/vinicius/Downloads/perf/sma_toad_input.png"
    "/home/vinicius/Downloads/perf/smw2_yoshi_01_input.png"
    "/home/vinicius/Downloads/perf/smw_boo_input.png"
    "/home/vinicius/Downloads/perf/smw_bowser_input.png"
    "/home/vinicius/Downloads/perf/splines test.png"
    "/home/vinicius/Downloads/perf/win31_386_input.png")

#files=("/home/vinicius/Downloads/perf/win31_386_input.png")

run_depixelize() {
    BIN="$(realpath src/depixelize-kopf2011/depixelize-kopf2011)"

    for f in "${files[@]}"; do
        echo "[${1}]" "${BIN}" "$f" -o /dev/null -v
        "${BIN}" "$f" -o /dev/null -v

        echo "[${1}]" "${BIN}" "$f" -o /dev/null -g
        "${BIN}" "$f" -o /dev/null -g

        echo "[${1}]" "${BIN}" "$f" -o /dev/null -n
        "${BIN}" "$f" -o /dev/null -n

        echo "[${1}]" "${BIN}" "$f" -o /dev/null
        "${BIN}" "$f" -o /dev/null
    done
}

addresssanitizer() {
    export ASAN_OPTIONS="detect_leaks=1"
    export LSAN_OPTIONS="suppressions=suppr.txt"

    mkdir -p address
    pushd address

    echo "leak:popt" > suppr.txt

    cmake -DCMAKE_CXX_COMPILER="clang++" -DCMAKE_BUILD_TYPE="Debug" -DCMAKE_CXX_FLAGS="-fsanitize=address -fno-omit-frame-pointer -O1 -fno-optimize-sibling-calls" ../..
    make

    run_depixelize "ADDRESS"

    popd
}

memorysanitizer() {
    mkdir -p memory
    pushd memory

    cmake -DCMAKE_CXX_COMPILER="clang++" -DCMAKE_BUILD_TYPE="Debug" -DCMAKE_CXX_FLAGS="-fsanitize=memory -fno-omit-frame-pointer -O1 -fno-optimize-sibling-calls" ../..
    make

    run_depixelize "MEMORY"

    popd
}

mkdir -p builds
pushd builds

addresssanitizer
#memorysanitizer

popd
rm -r builds
