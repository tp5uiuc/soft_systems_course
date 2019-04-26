#!bin/bash

usage() {
  cat <<EOM
    Usage:
    $(basename $0) <foldername>
	foldername is the directory containing your .pov files
EOM
  exit 0
}


main() {
  # set up working variables
  dir="$1"
  if [ ! -d "$dir" ]; then
	printf '%s\n' "${dir} does not exist" >&2
	# write error message to stderr
	exit 1
  fi

  startfolder=$(pwd)
  scenename=snake
  scenefolder=scenes
  scene=./${scenefolder}/${scenename}.inc
  images=${startfolder}/test_images/
  res_width=800
  res_height=450

  # prepare image folder
  if [ -d "$images" ];then
	rm -rf $images;
  fi
  mkdir -p $images

  # copy into simulation folder all files needed by povray
  cp $scene $dir

  # go into simulation folder
  cd $dir

  # in all povray files replace the default include file with the appropriate one
  # sed is installed by default in all nix systems
  sedstring=s/scenepovray/${scenename}/g
  sed -i -e ${sedstring} *.pov

  # loop over all povray files and produce images
  set +f
  for f in *.pov; do
	echo "processing ${f} file..."

	# Uses Parameter expansion
	# Read here if more interested
	# https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
	filenameonly=${f##*/}
	filenamenoext=${filenameonly%.*}

	# Run povray and move
	povray -h${res_height}-w${res_width} quality=11 antialias=on ${filenameonly}
	mv ${filenamenoext}.png $images

  done

  cd ${images}

  ffmpeg -s ${res_width}x${res_height} -pattern_type glob -i '*.png' -vcodec libx264 -framerate 30 -pix_fmt yuv420p snake.mp4

  # go back to original folder
  cd -
}

[ "$#" -ne 1 ] && ( usage && exit 1 ) || main $1
