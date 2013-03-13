#
# image count by bucket
#
# written by Klinginsmith, Jonathan Alan <jklingin@indiana.edu>
# Apr 30, 2012
import subprocess

def main():
    bucket_dict = {}
    output = subprocess.check_output("euca-describe-images")

    # Split the output by end-of-line chars.
    lines = output.split("\n")
    # Loop through lines. The image path is the third item.
    # Split by "/" to get bucket and key.
    for line in lines:
        if line:
            values = line.split()
            bucket, key = values[2].split("/")
            count = bucket_dict.get(bucket, 0)
            bucket_dict[bucket] = count + 1

    for key, value in bucket_dict.items():
        print("\t".join([key, str(value)]))

if __name__ == "__main__":
    main()
