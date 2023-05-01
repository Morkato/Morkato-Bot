const formatter = /(\$(?<key>[^ \n\t]+))/g
const text = "$test $abd"

for(let tex of text.matchAll(formatter))
  console.log(tex);