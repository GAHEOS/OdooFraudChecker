#!/bin/zsh
echo "########################################################"
echo "#############           clone.sh           #############"
echo "############# `date` #############"
echo "########################################################"
cat repositories.tsv | sed "s/\t/ /g" | while IFS=" " read -r repo_dir repo_url repo_commit
do
  git clone $repo_url -b 14.0
  cd $repo_dir
  git reset --hard $repo_commit
  cd ..
done
