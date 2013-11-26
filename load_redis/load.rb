#!/usr/bin/env ruby

def gen_redis_proto(*cmd)
    proto = ""
    proto << "*"+cmd.length.to_s+"\r\n"
    cmd.each{|arg|
        proto << "$"+arg.to_s.bytesize.to_s+"\r\n"
        proto << arg.to_s+"\r\n"
    }
    proto
end

file = File.new("out", "r")
while (line = file.gets)
  data = line.chomp("\n").split(' ', 2)
  STDOUT.write(gen_redis_proto("LPUSH", data[0], data[1]))
end
file.close
