import dns.resolver
from termcolor import colored, cprint
import pyfiglet
import os
from test import send_spoofed_email
import datetime


def check_dmarc_policy(domain):
    try:
        answers = dns.resolver.resolve(f"_dmarc.{domain}", "TXT")
        for record in answers:
            txt_record = str(record).strip('"')
            if "v=DMARC1" in txt_record:
                policy = None
                for part in txt_record.split(";"):
                    if part.strip().startswith("p="):
                        policy = part.split("=")[1].strip()
                        break
                return {"policy": policy, "full_record": txt_record}
        # If DMARC exists but no policy is found
        return {"policy": "DMARC exists, no policy", "full_record": txt_record}
    except dns.resolver.NoAnswer:
        return {"policy": None, "full_record": None}  # No DMARC record found
    except dns.resolver.NXDOMAIN:
        return {"policy": None, "full_record": None}  # Domain doesn't exist
    except dns.resolver.Timeout:
        print(
            colored(f"Timeout error for {domain}. DNS resolution took too long.", "red")
        )
        return {"policy": None, "full_record": None}
    except Exception as e:
        print(colored(f"Error checking DMARC for {domain}: {e}", "red"))
        return {"policy": None, "full_record": None}


def check_spf_record(domain):
    try:
        answers = dns.resolver.resolve(domain, "TXT")
        for record in answers:
            txt_record = str(record).strip('"')
            if "v=spf1" in txt_record:
                return txt_record
        return None  # No SPF record found
    except dns.resolver.NoAnswer:
        return None
    except dns.resolver.NXDOMAIN:
        return None
    except dns.resolver.Timeout:
        print(
            colored(f"Timeout error for {domain}. DNS resolution took too long.", "red")
        )
        return None
    except Exception as e:
        print(colored(f"Error checking SPF for {domain}: {e}", "red"))
        return None


def log_domain_scan(domain, dmarc_policy, spf_record, log_file="log.csv"):
    try:
        # Check if the file exists
        file_exists = os.path.isfile(log_file)

        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Prepare the log entry using commas as delimiters
        log_entry = f"{timestamp}, {domain}, {dmarc_policy}, {spf_record}\n"

        # Write the log entry to the log file in append mode
        with open(log_file, "a") as file:
            # Write header if the file didn't exist before
            if not file_exists:
                file.write("Timestamp, Domain, DMARC Policy, SPF Record\n")

            file.write(log_entry)

        print(f"{domain} added to log")

    except Exception as e:
        print(colored(f"Error logging to file: {e}", "red"))


def main():
    domains_input = input(
        "Please enter the domains you want to check (comma-separated): "
    )
    domains = [domain.strip() for domain in domains_input.split(",")]

    results = {}

    for domain in domains:
        dmarc_info = check_dmarc_policy(domain)
        spf_record = check_spf_record(domain)
        log_domain_scan(domain, dmarc_info["policy"], spf_record)  # Adjust logging
        full_dmarc_record = dmarc_info["full_record"] if dmarc_info else None

        results[domain] = {
            "DMARC": dmarc_info["policy"],
            "SPF": spf_record,
            "Full DMARC": full_dmarc_record,
        }

    header = pyfiglet.figlet_format("DMAbyuRC and SPF Check Report", font="slant")
    print(colored(header, "cyan", attrs=["bold"]))

    domain_counter = 1

    for domain, records in results.items():
        dmarc_policy = records["DMARC"]
        spf_record = records["SPF"]
        full_dmarc_record = records["Full DMARC"]
        bold_domain = f"\033[1m{domain}\033[0m"

        print(colored(f"{domain_counter}: {bold_domain}: ", "yellow"))
        domain_counter += 1
        if dmarc_policy:
            print(colored(f"    Full DMARC Record = {full_dmarc_record}", "blue"))
            print(colored(f"    DMARC Policy = {dmarc_policy}", "green"))
        else:
            print(colored("    No DMARC Policy found", "red"))

        if spf_record:
            print(colored(f"    SPF Record = {spf_record}", "blue"))
            print()
        else:
            print(colored("    No SPF Record found", "red"))

        # Handle DMARC issues
        bold_domain = f"\033[1m{domain}\033[0m"
        if dmarc_policy == "none" or dmarc_policy == "No DMARC Policy found":
            cprint(
                f"DMARC issue found for {bold_domain}! DMARC Policy not being enforced",
                "red",
                "on_red",
            )

            print()
            user_input = input(
                "Choose how to proceed:\n1. Send out email (Test Email Spoofing)\n2. Next\n> "
            )
            print()

            while user_input not in ["1", "2"]:
                user_input = input(
                    "Choose how to proceed:\n1. Send out email (Test Email Spoofing)\n2. Next\n> "
                )

            if user_input == "1":
                spoofed_sender_email = f"president@{domain}"
                recipient_email = (
                    "jojo.jensen03@gmail.com"  # CHANGE YOUR EMAIL ADDRESS HERE!!!
                )
                send_spoofed_email(spoofed_sender_email, recipient_email)
            elif user_input == "2":
                print("Moving onto the next.")
                continue
        else:
            print()
            cprint(f"No issues found in {bold_domain} at the moment!", "blue")
            print()
            print("-" * 50)


if __name__ == "__main__":
    main()
