#!/opt/homebrew/bin/bash

# Color definitions
reset="\033[0m"
red="\033[1;31m"
green="\033[1;32m"
yellow="\033[1;33m"
blue="\033[1;34m"
purple="\033[1;35m"
cyan="\033[1;36m"
white="\033[1;37m"

# Unicode box drawing characters
topleft="┌"
topright="┐"
bottomleft="└"
bottomright="┘"
vertical="│"
horizontal="─"
vertright="├"
horizdown="┬"
vertleft="┤"
horizup="┴"
cross="┼"


fancymessage() {
  message="$1"
  color="$2"
  max_per_line=40

  lines=()

  #
  # Split input by newline, then fold each line separately
  #
  # Outer loop breaks on each newline.
  #
  # The fold command will truncate lines with -s so that
  # words are not broken and also uses -w to limit the
  # number of characters in each line to max_per_line.
  #
  while IFS= read -r raw_line; do
    while IFS= read -r folded_line; do
      lines+=("$folded_line")
    done < <(echo "$raw_line" | fold -s -w $max_per_line)
  done < <(echo -e "$message")

  # Determine the box width (including padding of 2 spaces)
  box_width=$((max_per_line + 2))
  printf "$color"

  # Top border
  echo -n "$topleft"
  for ((i = 0; i < box_width; i++)); do
    echo -n "$horizontal"
  done
  echo "$topright"

  # Message lines, left-aligned
  for line in "${lines[@]}"; do
    line_len=${#line}
    right_padding=$((max_per_line - line_len))
    printf "$vertical %s%${right_padding}s %s\n" "$line" "" "$vertical"
  done

  # Bottom border
  echo -n "$bottomleft"
  for ((i = 0; i < box_width; i++)); do
    echo -n "$horizontal"
  done
  echo "$bottomright"

  # Reset color
  printf "\033[0m"
}



# Function to create a fancy table
fancy_table() {
    local title="$1"
    local title_color="$2"
    local header_color="$3"
    local data_color="$4"
    local column_headers=("${!5}")
    local data=("${!6}")

    local num_columns=${#column_headers[@]}
    local column_widths=()
    local total_width=1  # Start with 1 for the first vertical bar

    # Calculate column widths based on the longest content in each column
    for ((i=0; i<num_columns; i++)); do
        local max_width=${#column_headers[i]}

        # Check all data rows for this column
        for row in "${data[@]}"; do
            IFS='|' read -ra columns <<< "$row"
            local cell_content="${columns[i]}"

            if [ ${#cell_content} -gt $max_width ]; then
                max_width=${#cell_content}
            fi
        done

        # Add padding (3 spaces on each side)
        column_widths+=($((max_width + 6)))
        total_width=$((total_width + column_widths[i] + 1))  # +1 for the vertical bar
    done

    # Print title section
    printf "$title_color"
    echo -n "$topleft"
    for ((i=0; i<total_width-2; i++)); do
        echo -n "$horizontal"
    done
    echo "$topright"

    # Calculate title padding
    local title_padding=$(( (total_width - ${#title} - 2) / 2 ))
    local extra_space=$(( (total_width - ${#title} - 2) % 2 ))

    # Print title centered
    echo -n "$vertical"
    for ((i=0; i<title_padding; i++)); do
        echo -n " "
    done
    echo -n "$title"
    for ((i=0; i<title_padding+extra_space; i++)); do
        echo -n " "
    done
    echo "$vertical"

    # Print header section
    printf "$header_color"
    echo -n "$vertright"

    # Column headers separator line
    for ((col=0; col<num_columns; col++)); do
        for ((i=0; i<column_widths[col]; i++)); do
            echo -n "$horizontal"
        done
        if [ $col -lt $((num_columns-1)) ]; then
            echo -n "$horizdown"
        else
            echo "$vertleft"
        fi
    done

    # Print column headers
    echo -n "$vertical"
    for ((col=0; col<num_columns; col++)); do
        local pad_left=$(( (column_widths[col] - ${#column_headers[col]}) / 2 ))
        local pad_right=$(( column_widths[col] - ${#column_headers[col]} - pad_left ))

        for ((i=0; i<pad_left; i++)); do
            echo -n " "
        done
        echo -n "${column_headers[col]}"
        for ((i=0; i<pad_right; i++)); do
            echo -n " "
        done
        echo -n "$vertical"
    done
    echo

    # Header/Data separator
    echo -n "$vertright"
    for ((col=0; col<num_columns; col++)); do
        for ((i=0; i<column_widths[col]; i++)); do
            echo -n "$horizontal"
        done
        if [ $col -lt $((num_columns-1)) ]; then
            echo -n "$cross"
        else
            echo "$vertleft"
        fi
    done

    # Print data rows
    printf "$data_color"
    local row_count=${#data[@]}
    for ((row=0; row<row_count; row++)); do
        IFS='|' read -ra row_data <<< "${data[row]}"

        # Print each row
        echo -n "$vertical"
        for ((col=0; col<num_columns; col++)); do
            local content="${row_data[col]}"

            local pad_left=3  # Left padding always 3 spaces
            local pad_right=$((column_widths[col] - ${#content} - pad_left))

            for ((i=0; i<pad_left; i++)); do
                echo -n " "
            done
            echo -n "$content"
            for ((i=0; i<pad_right; i++)); do
                echo -n " "
            done
            echo -n "$vertical"
        done
        echo

        # Row separator (except for the last row)
        if [ $row -lt $((row_count-1)) ]; then
            echo -n "$vertright"
            for ((col=0; col<num_columns; col++)); do
                for ((i=0; i<column_widths[col]; i++)); do
                    echo -n "$horizontal"
                done
                if [ $col -lt $((num_columns-1)) ]; then
                    echo -n "$cross"
                else
                    echo "$vertleft"
                fi
            done
        fi
    done

    # Bottom border
    echo -n "$bottomleft"
    for ((col=0; col<num_columns; col++)); do
        for ((i=0; i<column_widths[col]; i++)); do
            echo -n "$horizontal"
        done
        if [ $col -lt $((num_columns-1)) ]; then
            echo -n "$horizup"
        else
            echo "$bottomright"
        fi
    done

    # Reset color
    printf "$reset"
}

# Function to get simplified Git repository stats
get_git_stats() {
    local repo_name="$(git remote -v 2>/dev/null | head -n1 | awk '{print $2}' | sed 's/.*\///' | sed 's/\.git//')"

    if [ -z "$repo_name" ]; then
        repo_name="Current Git Repository"
    fi

    local total_commits=$(git rev-list --count origin/main 2>/dev/null)
    if [ -z "$total_commits" ]; then
        echo "Not a git repository or no commits found."
        exit 1
    fi

    # Get contributor stats - just name and commit count
    mapfile -t git_stats < <(git log origin/main --pretty="%aN" | sort | uniq -c | sort -rn)

    # Format contributor data for table - just 3 columns
    local contributor_data=()
    local index=1

    for line in "${git_stats[@]}"; do
        count=$(echo "$line" | awk '{print $1}')
        name=$(echo "$line" | awk '{print $2}')

        contributor_data+=("$index|$name|$count")
        ((index++))
    done

    # Set column headers for the simplified table
    column_headers=("Rank" "Contributor" "Commits")

    # Display the table with repo info
    fancymessage "$(echo -e "Repository Name\t$repo_name\nTotal Commits\t$total_commits commits" | column -t -s$'\t')" "$green"
    echo

    # Pass arrays by reference (indirectly)
    fancy_table "GIT REPOSITORY CONTRIBUTORS" "$green" "$green" "$blue" column_headers[@] contributor_data[@]
}

# Main execution
get_git_stats
